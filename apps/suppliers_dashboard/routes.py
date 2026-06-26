# coding: utf-8
# 📂 apps/suppliers_dashboard/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

# تعريف البلوبرينت بوضوح
# الاسم 'suppliers_dashboard' هو الذي سنستخدمه في url_for
dashboard_bp = Blueprint(
    'suppliers_dashboard', 
    __name__, 
    template_folder='templates'
)

@dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """
    لوحة التحكم الرئيسية للمورد:
    - يتم الوصول إليها عبر /suppliers/dashboard
    """
    # مثال لجلب البيانات (سنقوم بتحديثه لاحقاً حسب موديل الطلبات لديك)
    pending_orders_count = 0 
    
    return render_template(
        'suppliers/dashboard.html',
        pending_orders_count=pending_orders_count
    )

@dashboard_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """
    صفحة إعدادات المتجر.
    """
    return render_template('suppliers/settings.html')
