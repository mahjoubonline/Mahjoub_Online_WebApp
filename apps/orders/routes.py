# coding: utf-8
# 📂 apps/orders/routes.py

import traceback
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from apps.extensions import db
from apps.models.orders_db import Order
from apps.models.financials_db import OrderFinancial
from apps.api.sync_engine import SyncEngine

orders_bp = Blueprint('orders', __name__, template_folder='templates')

@orders_bp.route('/dashboard')
@login_required
def dashboard():
    """عرض لوحة تحكم الطلبات مع الفلاتر والتصفح."""
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # بناء الاستعلام مع الربط
    query = db.session.query(Order, OrderFinancial).outerjoin(OrderFinancial)
    
    # تطبيق الفلاتر
    q = request.args.get('q', '').strip()
    if q:
        query = query.filter(
            Order.order_id_display.contains(q) | 
            Order.customer_name.contains(q)
        )
    
    status = request.args.get('status', '').strip()
    if status:
        query = query.filter(Order.status == status)
        
    # التنفيذ
    pagination = query.order_by(Order.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    # إحصائيات آمنة (تم معالجة التشفير بحساب المجموع برمجياً)
    all_financials = OrderFinancial.query.all()
    total_sales = sum(fin.total_paid for fin in all_financials)
    
    stats = {
        'cancelled': Order.query.filter_by(status='cancelled').count(),
        'completed': Order.query.filter_by(status='completed').count(),
        'total_sales': total_sales
    }
    
    return render_template('admin/orders_dashboard.html', pagination=pagination, stats=stats)

@orders_bp.route('/sync-all', methods=['POST'])
@login_required
def sync_all():
    """دالة المزامنة."""
    try:
        success = SyncEngine.fetch_and_sync_order()
        if success:
            flash("تمت المزامنة وتحديث البيانات بنجاح", "success")
        else:
            flash("فشلت عملية المزامنة. يرجى مراجعة سجلات النظام.", "danger")
    except Exception as e:
        flash(f"حدث خطأ تقني: {str(e)}", "danger")
        traceback.print_exc()
        
    return redirect(url_for('orders.dashboard'))

@orders_bp.route('/view-order/<string:order_id>') 
@login_required
def view_order(order_id):
    """عرض تفاصيل طلب محدد."""
    result = db.session.query(Order, OrderFinancial)\
        .outerjoin(OrderFinancial, Order.id == OrderFinancial.order_id)\
        .filter(Order.id == order_id).first_or_404()
        
    return render_template('admin/order_details.html', order=result[0], financial=result[1])
