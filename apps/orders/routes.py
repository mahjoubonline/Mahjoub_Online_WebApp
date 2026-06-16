# coding: utf-8
# 📂 apps/orders/routes.py

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
import logging

# الاستيراد المطلق من محرك الطلبات
from apps.utils.orders_engine import get_pending_orders

# إعداد الـ logger
logger = logging.getLogger(__name__)

# تعريف الـ Blueprint باسم 'orders'
# template_folder='templates' تعني أن Flask يبحث في apps/orders/templates/
orders_bp = Blueprint('orders', __name__, template_folder='templates')

@orders_bp.route('/pending', methods=['GET'])
@login_required
def orders_dashboard():
    """عرض الطلبات المعلقة التي تحتاج تسوية"""
    try:
        # جلب البيانات من محرك الطلبات
        orders = get_pending_orders()
        
        # المسار الصحيح للملف داخل مجلد templates هو 'admin/orders_dashboard.html'
        # Flask سيبحث عنه في: apps/orders/templates/admin/orders_dashboard.html
        return render_template('admin/orders_dashboard.html', orders=orders)
        
    except Exception as e:
        logger.error(f"Error fetching pending orders: {str(e)}")
        # إرجاع رسالة خطأ واضحة أو صفحة خطأ
        return f"حدث خطأ أثناء جلب الطلبات: {str(e)}", 500

@orders_bp.route('/process/<order_id>', methods=['POST'])
@login_required
def process_order(order_id):
    """معالجة طلب معين"""
    # سيتم إضافة منطق الربط المالي هنا لاحقاً
    return jsonify({'success': True, 'message': f'تمت معالجة الطلب {order_id}'})
