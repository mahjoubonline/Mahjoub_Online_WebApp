# coding: utf-8
# 📂 apps/orders/routes.py - التحكم في مسارات الطلبات والمزامنة

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from apps.extensions import db
from apps.models.orders_db import ProcessedOrder, OrderItem
from apps.api.sync_engine import SyncEngine
import logging

# تعريف الـ Blueprint الخاص بالطلبات
orders_bp = Blueprint('orders', __name__, url_prefix='/orders')
logger = logging.getLogger(__name__)

# 1. لوحة تحكم الطلبات مع الترقيم (10 طلبات لكل صفحة)
@orders_bp.route('/dashboard')
def orders_dashboard():
    page = request.args.get('page', 1, type=int)
    # جلب الطلبات مرتبة من الأحدث للأقدم مع نظام الترقيم المدمج
    pagination = ProcessedOrder.query.order_by(ProcessedOrder.created_at_local.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    # تم إيقاف جلب الموردين مؤقتاً لتجنب خطأ ModuleNotFoundError
    suppliers = [] 
    return render_template('orders/dashboard.html', pagination=pagination, suppliers=suppliers)

# 2. المزامنة الشاملة (تستدعي محرك المزامنة)
@orders_bp.route('/sync-all', methods=['POST'])
def sync_all():
    try:
        # محاكاة لعملية المزامنة عبر SyncEngine
        if SyncEngine.fetch_and_sync_order():
            flash("تمت مزامنة الطلبات بنجاح من قمرة كلاود.", "success")
        else:
            flash("لم يتم العثور على طلبات جديدة للمزامنة.", "warning")
    except Exception as e:
        logger.error(f"Sync error: {e}")
        flash("حدث خطأ أثناء الاتصال بخادم المزامنة.", "danger")
    return redirect(url_for('orders.orders_dashboard'))

# 3. تحديث الحالات ديناميكياً (عبر AJAX)
@orders_bp.route('/update-order-field/<string:order_id>', methods=['POST'])
def update_order_field(order_id):
    data = request.get_json()
    field = data.get('field')
    value = data.get('value')
    
    order = ProcessedOrder.query.get_or_404(order_id)
    
    try:
        if hasattr(order, field):
            setattr(order, field, value)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'تم تحديث الحقل بنجاح'})
    except Exception as e:
        logger.error(f"خطأ في التحديث: {e}")
        db.session.rollback()
        
    return jsonify({'status': 'error', 'message': 'فشل تحديث البيانات'}), 400

# 4. تحديث المورد المحلي (عبر AJAX)
@orders_bp.route('/update-supplier/<string:order_id>', methods=['POST'])
def update_supplier(order_id):
    data = request.get_json()
    supplier_name = data.get('supplier_name') # تم التعديل ليتناسب مع الحقل النصي الجديد
    
    order = ProcessedOrder.query.get_or_404(order_id)
    order.supplier_name = supplier_name
    
    try:
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error'}), 400

# 5. عرض ومعالجة الطلب التفصيلي
@orders_bp.route('/process/<string:order_id>')
def process_order(order_id):
    order = ProcessedOrder.query.get_or_404(order_id)
    return render_template('orders/order_details.html', order=order)

# 6. إلغاء الطلب
@orders_bp.route('/cancel/<string:order_id>', methods=['POST'])
def cancel_order_route(order_id):
    order = ProcessedOrder.query.get_or_404(order_id)
    order.order_status = 'cancelled'
    try:
        db.session.commit()
        flash(f"تم إلغاء الطلب {order.order_id} بنجاح.", "info")
    except:
        db.session.rollback()
        flash("تعذر إلغاء الطلب، يرجى المحاولة لاحقاً.", "danger")
    return redirect(url_for('orders.orders_dashboard'))

# 7. مسار البحث
@orders_bp.route('/search')
def search_orders():
    query = request.args.get('q', '')
    orders = ProcessedOrder.query.filter(ProcessedOrder.customer_name.contains(query)).all()
    return render_template('orders/dashboard.html', pagination=None, orders=orders)
