# 📂 apps/orders/routes.py
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
import logging

# الاستيراد المطلق
from apps.utils.orders_engine import get_pending_orders

logger = logging.getLogger(__name__)

# تعريف الـ Blueprint باسم 'orders'
orders_bp = Blueprint('orders', __name__, template_folder='templates')

@orders_bp.route('/pending', methods=['GET'])
@login_required
def orders_dashboard():
    """عرض الطلبات المعلقة التي تحتاج تسوية"""
    try:
        # جلب البيانات من محرك الطلبات
        orders = get_pending_orders()
        # التأكد من المسار الصحيح للملف: orders/pending_list.html
        return render_template('orders/pending_list.html', orders=orders)
    except Exception as e:
        logger.error(f"Error fetching pending orders: {str(e)}")
        return jsonify({'error': 'حدث خطأ أثناء جلب الطلبات'}), 500

@orders_bp.route('/process/<order_id>', methods=['POST'])
@login_required
def process_order(order_id):
    """معالجة طلب معين"""
    # هنا سيتم إضافة منطق الربط المالي لاحقاً
    return jsonify({'success': True, 'message': f'تمت معالجة الطلب {order_id}'})
