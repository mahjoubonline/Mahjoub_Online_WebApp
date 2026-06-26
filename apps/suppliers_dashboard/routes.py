# coding: utf-8
# 📂 apps/suppliers_dashboard/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

# تعريف البلوبرينت
# تأكد أن الاسم هنا 'suppliers_dashboard' هو المستخدم في الـ Registry
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
    يتم الوصول إليها عبر المسار الموحد: /suppliers/dashboard
    """
    # مثال لجلب البيانات (سنقوم بتطويره لاحقاً)
    context = {
        'pending_orders_count': 0,
        'supplier_name': current_user.username if hasattr(current_user, 'username') else 'شريكنا العزيز'
    }
    
    # تأكد من أن الملف موجود في المسار: templates/suppliers/dashboard.html
    return render_template('suppliers/dashboard.html', **context)

@dashboard_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """
    صفحة إعدادات المتجر الخاصة بالمورد.
    """
    return render_template('suppliers/settings.html')
