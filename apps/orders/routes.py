# 📂 apps/orders/routes.py
from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
import logging

from apps.utils.orders_engine import get_pending_orders

logger = logging.getLogger(__name__)

orders_bp = Blueprint('orders', __name__, template_folder='templates')

@orders_bp.route('/pending', methods=['GET'])
@login_required
def orders_dashboard():
    """عرض الطلبات المعلقة في لوحة التحكم (القيادة المركزية)"""
    if not current_user.is_authenticated:
        return redirect(url_for('auth_portal.login'))
        
    try:
        orders = get_pending_orders()
        return render_template('admin/orders_dashboard.html', orders=orders)
    except Exception as e:
        logger.error(f"Error in orders_dashboard: {str(e)}")
        return render_template('admin/orders_dashboard.html', orders=[])
