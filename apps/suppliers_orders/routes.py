# coding: utf-8
# 📂 apps/suppliers_orders/routes.py

from flask import Blueprint, render_template, request, jsonify, abort, session
from flask_login import login_required, current_user
from apps.extensions import db
from apps.models.financials_db import OrderFinancial
from apps.api.sync_engine import SyncEngine  # استيراد محرك المزامنة المحاسبي
from sqlalchemy.orm import joinedload

# تعريف البلوبرينت باسم 'suppliers_orders' ليتطابق مع التسجيل التلقائي
suppliers_orders_bp = Blueprint('suppliers_orders', __name__, template_folder='templates')

@suppliers_orders_bp.route('/dashboard')
@login_required
def dashboard():
    """لوحة تحكم طلبات المورد (Pagination + Financials + Auto-Sync)"""
    # حماية: التأكد من أن المستخدم الحالي هو مورد
    if session.get('user_type') != 'supplier':
        abort(403)

    page = request.args.get('page', 1, type=int)
    
    # استعلام ذكي لجلب البيانات المالية مع الطلبات المرتبطة بها
    # نستخدم joinedload لتسريع الأداء ومنع استعلامات N+1
    pagination = OrderFinancial.query.filter_by(supplier_id=current_user.id)\
                        .options(joinedload(OrderFinancial.order))\
                        .order_by(OrderFinancial.created_at.desc())\
                        .paginate(page=page, per_page=20)
    
    # التحقق من طلب AJAX لتحديث الجدول فقط
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('admin/partials/_supplier_table.html', pagination=pagination)
        
    return render_template('admin/suppliers_orders_dashboard.html', 
                           pagination=pagination)

@suppliers_orders_bp.route('/order/complete/<order_id>', methods=['POST'])
@login_required
def complete_order(order_id):
    """عملية أتمتة إكمال الطلب وتحويل المستحقات للمحفظة عبر المحرك المالي"""
    # 1. البحث عن السجل المالي الخاص بالطلب والمورد الحالي فقط
    fin = OrderFinancial.query.filter_by(order_id=order_id, supplier_id=current_user.id).first_or_404()
    
    # 2. التحقق من حالة الطلب
    if fin.order.status == 'completed':
        return jsonify({'status': 'error', 'message': 'الطلب مكتمل مسبقاً'}), 400

    try:
        # 3. استخدام محرك المزامنة (SyncEngine) لضمان اتساق العمليات المالية
        # نمرر إجمالي القيمة ليقوم المحرك بتوزيع حصة المورد والمنصة
        success = SyncEngine.process_financials(
            order_id=fin.order_id,
            supplier_id=current_user.id,
            total_price=fin.total_paid, # القيمة الكلية للطلب
            product_currency=fin.currency
        )
        
        if success:
            # تحديث حالة الطلب ليكون مكتمل
            fin.order.status = 'completed'
            fin.settlement_status = 'settled'
            fin.settled_at = db.func.now()
            db.session.commit()
            
            return jsonify({'status': 'success', 'message': 'تم إكمال الطلب بنجاح'})
        else:
            return jsonify({'status': 'error', 'message': 'فشلت عملية التسوية المالية عبر المحرك'}), 500
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f"خطأ غير متوقع: {str(e)}"}), 500
