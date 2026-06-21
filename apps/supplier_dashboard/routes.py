# coding: utf-8
# 📂 apps/supplier_dashboard/routes.py

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from apps.models.supplier_db import Supplier
from apps.models.order_db import Order  # افترضنا وجود موديل للطلبات

# تعريف Blueprint الخاص بلوحة الموردين
supplier_bp = Blueprint(
    'supplier_dashboard', 
    __name__, 
    template_folder='templates',
    url_prefix='/supplier'
)

@supplier_bp.route('/dashboard')
@login_required
def dashboard():
    """لوحة تحكم المورد السيادية"""
    
    # التحقق من أن المستخدم مورد (اختياري، يمكنك إضافة شرط صلاحية هنا)
    supplier = current_user
    
    # جلب إحصائيات المورد (يتم الاعتماد على دالة بالموديل أو استعلام مباشر)
    # ملاحظة: تأكد من أنك تستخدم أسماء الأعمدة الفعلية في قاعدة البيانات وليس @property
    stats = {
        'total_sales': supplier.get_total_sales(), # دالة داخل الموديل
        'pending_orders': Order.query.filter_by(supplier_id=supplier.id, status='pending').count()
    }
    
    # جلب آخر 5 طلبات للمورد
    recent_orders = Order.query.filter_by(supplier_id=supplier.id)\
                               .order_by(Order.created_at.desc())\
                               .limit(5).all()
    
    return render_template(
        'supplier/supplier_content.html', 
        supplier_stats=stats, 
        recent_orders=recent_orders
    )

@supplier_bp.route('/products')
@login_required
def manage_products():
    """صفحة إدارة المنتجات للمورد"""
    return "صفحة إدارة المنتجات - قيد التطوير"

@supplier_bp.route('/financials')
@login_required
def financials():
    """كشف الحساب المالي للمورد"""
    return "كشف الحساب المالي للمورد - قيد التطوير"
