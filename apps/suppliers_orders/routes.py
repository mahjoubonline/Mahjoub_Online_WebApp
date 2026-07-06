# coding: utf-8
# 📂 apps/suppliers_orders/routes.py

import os
from flask import Blueprint, render_template, abort, session, request
from flask_login import login_required, current_user

# تعريف الـ Blueprint
suppliers_orders_bp = Blueprint('suppliers_orders', __name__, template_folder='templates')

# إضافة مسار قوالب الداشبورد لتجنب خطأ TemplateNotFound
base_templates_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../suppliers_dashboard/templates'))
suppliers_orders_bp.jinja_loader.searchpath.append(base_templates_path)

@suppliers_orders_bp.route('/index', methods=['GET'])
@login_required
def index():
    """
    نافذة شاملة تعرض طلبات المورد مع نظام ترقيم صفحات لدعم الأداء العالي.
    """
    from apps.models.orders_db import Order
    
    user_type = session.get('user_type')
    # تحديد معرف المورد
    s_id = current_user.id if user_type == 'supplier' else getattr(current_user, 'supplier_id', None)
    
    if not s_id:
        abort(403)

    # الحصول على رقم الصفحة من الطلب (الافتراضي 1)
    page = request.args.get('page', 1, type=int)
    
    # استخدام paginate لتحسين الأداء (10 طلبات لكل صفحة)
    pagination = Order.query.filter_by(supplier_id=s_id).order_by(Order.id.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    # دعم التحديث الجزئي عبر AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('admin/partials/_supplier_table.html', pagination=pagination)
        
    return render_template('admin/suppliers_orders_dashboard.html', pagination=pagination)

@suppliers_orders_bp.route('/details/<int:order_id>', methods=['GET'])
@login_required
def order_details(order_id):
    from apps.models.orders_db import Order
    
    order = Order.query.get_or_404(order_id)
    
    user_type = session.get('user_type')
    s_id = current_user.id if user_type == 'supplier' else getattr(current_user, 'supplier_id', None)
    
    # التحقق من أن الطلب يخص المورد الحالي فقط
    if order.supplier_id != s_id:
        abort(403)
        
    return render_template('admin/order_details.html', order=order)
