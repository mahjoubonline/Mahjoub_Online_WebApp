# coding: utf-8
# 📂 apps/orders/routes.py - التحكم في مسارات الطلبات والمزامنة

import os
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from apps.extensions import db
from apps.models.orders_db import ProcessedOrder
from apps.api.sync_engine import SyncEngine
import logging

# تعريف الـ Blueprint مع تحديد مجلد القوالب المحلي الخاص به
# يضمن هذا أن Flask سيعثر على القالب في: apps/orders/templates/admin/
orders_bp = Blueprint(
    'orders', 
    __name__, 
    url_prefix='/orders', 
    template_folder='templates'
)
logger = logging.getLogger(__name__)

# 1. لوحة تحكم الطلبات
@orders_bp.route('/dashboard')
def orders_dashboard():
    try:
        page = request.args.get('page', 1, type=int)
        # جلب الطلبات مرتبة من الأحدث للأقدم
        pagination = ProcessedOrder.query.order_by(ProcessedOrder.created_at_local.desc()).paginate(
            page=page, per_page=10, error_out=False
        )
        return render_template('admin/orders_dashboard.html', pagination=pagination)
    except Exception as e:
        logger.error(f"Dashboard Error: {e}")
        return f"خطأ في تحميل لوحة التحكم: {str(e)}", 500

# 2. المزامنة الشاملة
@orders_bp.route('/sync-all', methods=['POST'])
def sync_all():
    try:
        if SyncEngine.fetch_and_sync_order():
            flash("تمت مزامنة الطلبات بنجاح من قمرة كلاود.", "success")
        else:
            flash("لم يتم العثور على طلبات جديدة للمزامنة.", "warning")
    except Exception as e:
        logger.error(f"Sync error: {e}")
        flash("حدث خطأ أثناء الاتصال بخادم المزامنة.", "danger")
    return redirect(url_for('orders.orders_dashboard'))

# 3. تحديث الحالات ديناميكياً (AJAX)
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
            return jsonify({'status': 'success', 'message': 'تم التحديث بنجاح'})
    except Exception as e:
        logger.error(f"Update error: {e}")
        db.session.rollback()
    return jsonify({'status': 'error', 'message': 'فشل التحديث'}), 400

# 4. تحديث المورد المحلي (AJAX)
@orders_bp.route('/update-supplier/<string:order_id>', methods=['POST'])
def update_supplier(order_id):
    data = request.get_json()
    supplier_name = data.get('supplier_name')
    order = ProcessedOrder.query.get_or_404(order_id)
    order.supplier_name = supplier_name
    try:
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400

# 5. عرض ومعالجة الطلب التفصيلي
@orders_bp.route('/process/<string:order_id>')
def process_order(order_id):
    order = ProcessedOrder.query.get_or_404(order_id)
    return render_template('admin/order_details.html', order=order)

# 6. إلغاء الطلب
@orders_bp.route('/cancel/<string:order_id>', methods=['POST'])
def cancel_order_route(order_id):
    order = ProcessedOrder.query.get_or_404(order_id)
    order.order_status = 'cancelled'
    try:
        db.session.commit()
        flash(f"تم إلغاء الطلب {order.order_id} بنجاح.", "info")
    except Exception as e:
        db.session.rollback()
        flash("تعذر إلغاء الطلب، يرجى المحاولة لاحقاً.", "danger")
    return redirect(url_for('orders.orders_dashboard'))

# 7. مسار البحث
@orders_bp.route('/search')
def search_orders():
    query = request.args.get('q', '')
    orders = ProcessedOrder.query.filter(ProcessedOrder.customer_name.contains(query)).all()
    # يتم العرض بنفس القالب المستخدم في لوحة التحكم
    return render_template('admin/orders_dashboard.html', pagination=None, orders=orders)
