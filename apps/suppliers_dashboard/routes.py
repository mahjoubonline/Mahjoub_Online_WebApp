# coding: utf-8
# 📂 apps/suppliers_dashboard/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

# تعريف البلوبرينت
# تأكد أن هذا الاسم 'suppliers_dashboard' هو المستخدم في الـ Registry
dashboard_bp = Blueprint(
    'suppliers_dashboard', 
    __name__, 
    template_folder='templates'
)

@dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """
    لوحة التحكم الرئيسية للمورد.
    يتم الوصول إليها عبر: /suppliers/dashboard
    """
    # التحقق من أن المستخدم الحالي هو مورد (اختياري، لزيادة الأمان)
    # if not hasattr(current_user, 'supplier_id'):
    #     return redirect(url_for('suppliers_auth.login'))

    # جلب بيانات الطلبات (سيتم تحديثها لاحقاً)
    pending_orders_count = 0 
    
    return render_template(
        'suppliers/dashboard.html',
        pending_orders_count=pending_orders_count
    )

@dashboard_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """
    صفحة إعدادات المتجر الخاصة بالمورد.
    """
    return render_template('suppliers/settings.html')
