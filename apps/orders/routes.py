# 📂 apps/orders/routes.py
from flask import Blueprint, render_template, request, jsonify
from apps.utils.orders_engine import OrdersEngine
from flask_login import login_required
import logging

logger = logging.getLogger(__name__)

# تعريف الـ Blueprint
orders_bp = Blueprint('orders', __name__, template_folder='templates')

@orders_bp.route('/admin/orders', methods=['GET'])
@login_required
def orders_dashboard():
    """عرض لوحة التحكم الخاصة بالطلبات"""
    try:
        columns = [
            {'label': 'رقم الطلب', 'key': 'order_id_qumra'},
            {'label': 'العميل', 'key': 'customer_name'},
            {'label': 'الإجمالي', 'key': 'total'},
            {'label': 'الحالة', 'key': 'status'},
            {'label': 'التاريخ', 'key': 'created_at'}
        ]
        engine = OrdersEngine()
        page = request.args.get('page', 1, type=int)
        pagination = engine.get_paginated_orders(page=page)
        
        return render_template(
            'admin/orders_dashboard.html', 
            orders=pagination.items, 
            pagination=pagination,
            columns=columns
        )
    except Exception as e:
        logger.exception("Error loading orders dashboard")
        return "حدث خطأ داخلي", 500

@orders_bp.route('/sync-orders', methods=['POST'])
@login_required
def sync_orders():
    """مسار مزامنة الطلبات"""
    try:
        engine = OrdersEngine()
        count = engine.sync_orders_from_source()
        return jsonify({'success': True, 'message': f'تم جلب {count} طلب'})
    except Exception as e:
        logger.error(f"Sync error: {str(e)}")
        return jsonify({'success': False, 'message': 'فشل الاتصال'}), 500

@orders_bp.route('/update-status', methods=['POST'])
@login_required
def update_order_status():
    """مسار تحديث حالة الطلب"""
    try:
        data = request.json
        engine = OrdersEngine()
        success = engine.update_status(data.get('orderId'), data.get('value'))
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'success': False}), 500
