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
    """لوحة تحكم الطلبات"""
    try:
        # تعريف الأعمدة: يجب أن تتطابق 'key' مع أسماء الحقول في الـ Model أو الـ Dict
        columns = [
            {'label': 'رقم الطلب', 'key': 'order_id_qumra'},
            {'label': 'العميل', 'key': 'customer_name'},
            {'label': 'الإجمالي', 'key': 'total'},
            {'label': 'حالة الطلب', 'key': 'status'},
            {'label': 'التاريخ', 'key': 'created_at'}
        ]
        
        engine = OrdersEngine()
        page = request.args.get('page', 1, type=int)
        pagination = engine.get_paginated_orders(page=page)
        
        return render_template(
            'admin/orders_dashboard.html', 
            orders=pagination.items, 
            pagination=pagination,
            columns=columns # تمرير الأعمدة للقالب
        )
    except Exception as e:
        logger.exception("Error loading orders dashboard")
        return f"حدث خطأ أثناء تحميل لوحة الطلبات: {str(e)}", 500
