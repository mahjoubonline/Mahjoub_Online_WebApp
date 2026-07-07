# coding: utf-8
# 📂 apps/suppliers_orders/routes.py

import os
from flask import Blueprint, render_template, abort, session, request
from flask_login import login_required, current_user
from apps.models.orders_db import Order
from apps.orders.services import OrderService # استيراد الخدمة الجديدة

# تعريف الـ Blueprint
suppliers_orders_bp = Blueprint('suppliers_orders', __name__, template_folder='templates')

# إضافة مسار قوالب الداشبورد لتجنب خطأ TemplateNotFound
base_templates_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../suppliers_dashboard/templates'))
suppliers_orders_bp.jinja_loader.searchpath.append(base_templates_path)

@suppliers_orders_bp.route('/index', methods=['GET'])
@login_required
def index():
    """
    نافذة شاملة تعرض طلبات المورد مع نظام ترقيم صفحات.
    """
    user_type = session.get('user_type')
    # تحديد معرف المورد (نستخدم int للبحث في قاعدة البيانات)
    s_id = current_user.id if user_type == 'supplier' else getattr(current_user, 'supplier_id', None)
    
    if s_id is None:
        abort(403)

    page = request.args.get('page', 1, type=int)
    
    # استخدام الاستعلام المباشر مع تمرير المتغيرات المطلوبة للقالب
    pagination = Order.query.filter_by(supplier_id=int(s_id)).order_by(Order.id.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    # التعديل الهام هنا: تمرير pagination.items باسم 'orders' للقالب
    context = {
        'orders': pagination.items, 
        'pagination': pagination
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('admin/partials/_supplier_table.html', **context)
        
    return render_template('admin/suppliers_orders_dashboard.html', **context)

@suppliers_orders_bp.route('/details/<string:order_id>', methods=['GET'])
@login_required
def order_details(order_id):
    """
    عرض تفاصيل طلب معين باستخدام خدمة الطلبات.
    """
    # استخدام الخدمة لجلب البيانات (التي تعالج الربط المالي أيضاً)
    order, financial = OrderService.get_order_details(order_id)
    
    if not order:
        abort(404)
    
    user_type = session.get('user_type')
    s_id = current_user.id if user_type == 'supplier' else getattr(current_user, 'supplier_id', None)
    
    # التحقق من الصلاحيات
    if str(order.supplier_id) != str(s_id):
        abort(403)
        
    return render_template('admin/order_details.html', order=order, financial=financial)
