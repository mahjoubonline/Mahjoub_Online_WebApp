# coding: utf-8
# 📂 apps/suppliers_orders/routes.py

from flask import Blueprint, render_template, request, session, abort
from flask_login import login_required, current_user

# --- ملاحظة هامة جداً ---
# لا تستورد هنا أي شيء من apps.extensions أو apps.models مباشرة في أعلى الملف
# إذا كنت تحتاج لنماذج البيانات (models)، استوردها داخل الدوال فقط.

# تعريف الـ Blueprint
suppliers_orders_bp = Blueprint('suppliers_orders', __name__, template_folder='templates')

@suppliers_orders_bp.route('/index', methods=['GET'])
@login_required
def index():
    """عرض قائمة طلبات المورد"""
    # استيراد النماذج هنا لتجنب Circular Import
    from apps.models.orders_db import Order
    from apps.models.supplier_db import Supplier
    
    user_type = session.get('user_type')
    s_id = current_user.id if user_type == 'supplier' else getattr(current_user, 'supplier_id', None)
    
    if not s_id:
        abort(403)

    # مثال لجلب الطلبات
    orders = Order.query.filter_by(supplier_id=s_id).all()
    
    return render_template('suppliers/orders.html', orders=orders)

@suppliers_orders_bp.route('/details/<int:order_id>', methods=['GET'])
@login_required
def order_details(order_id):
    from apps.models.orders_db import Order
    
    order = Order.query.get_or_404(order_id)
    
    # التحقق من الصلاحية
    user_type = session.get('user_type')
    s_id = current_user.id if user_type == 'supplier' else getattr(current_user, 'supplier_id', None)
    
    if order.supplier_id != s_id:
        abort(403)
        
    return render_template('suppliers/order_details.html', order=order)
