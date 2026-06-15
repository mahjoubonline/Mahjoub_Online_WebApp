# 📂 apps/orders/routes.py
from flask import Blueprint, render_template, request, jsonify
from apps.utils.orders_engine import OrdersEngine
from flask_login import login_required
import logging

logger = logging.getLogger(__name__)

# اسم الـ Blueprint هنا هو 'orders' ليتطابق مع url_for('orders.orders_dashboard') في الواجهة
orders_bp = Blueprint('orders', __name__, template_folder='templates')

@orders_bp.route('/admin/orders', methods=['GET'])
@login_required
def orders_dashboard():
    """لوحة تحكم الطلبات"""
    try:
        engine = OrdersEngine()
        # نفترض أن engine.get_paginated_orders يعيد كائنات Pagination
        page = request.args.get('page', 1, type=int)
        pagination = engine.get_paginated_orders(page=page)
        
        return render_template(
            'admin/orders_dashboard.html', 
            orders=pagination.items, 
            pagination=pagination
        )
    except Exception as e:
        logger.error(f"Error loading orders dashboard: {str(e)}")
        return "حدث خطأ أثناء تحميل لوحة الطلبات", 500

@orders_bp.route('/api/sync', methods=['POST'])
@login_required
def sync_orders():
    """مزامنة الطلبات"""
    try:
        engine = OrdersEngine()
        result = engine.sync_orders_from_source()
        return jsonify({'success': True, 'message': 'تمت المزامنة بنجاح'})
    except Exception as e:
        logger.error(f"Error syncing orders: {str(e)}")
        return jsonify({'success': False, 'message': 'فشل المزامنة'}), 500
