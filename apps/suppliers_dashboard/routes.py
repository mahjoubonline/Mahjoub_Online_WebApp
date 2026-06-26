# coding: utf-8
# 📂 apps/suppliers_dashboard/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from apps.models.supplier_staff_db import SupplierStaff # الموديل المعتمد للموردين

# تعريف البلوبرينت
dashboard_bp = Blueprint(
    'suppliers_dashboard', 
    __name__, 
    template_folder='templates'
)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    """
    لوحة التحكم الرئيسية للمورد:
    - تعرض رصيد المحفظة.
    - تعرض عدد الطلبات المعلقة.
    """
    # التحقق من صلاحية الوصول (يمكن إضافة شرط إذا كان المورد موقوفاً)
    
    # جلب الطلبات (بافتراض وجود علاقة أو استعلام)
    # ملاحظة: استبدل `pending_orders_count` بالاستعلام الفعلي من قاعدة بيانات الطلبات لديك
    pending_orders_count = 0 # يمكنك إضافة: Order.query.filter_by(supplier_id=current_user.id, status='pending').count()
    
    return render_template(
        'suppliers/dashboard.html',
        pending_orders_count=pending_orders_count
    )

@dashboard_bp.route('/settings')
@login_required
def settings():
    """
    صفحة إعدادات المتجر الخاصة بالمورد.
    """
    return render_template('suppliers/settings.html')

# يمكنك إضافة المزيد من المسارات هنا (كشف الحساب، الطلبات، إلخ)
