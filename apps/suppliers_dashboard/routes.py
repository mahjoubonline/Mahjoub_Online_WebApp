# coding: utf-8
# 📂 apps/suppliers_dashboard/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from apps.models.supplier_db import Supplier

# تعريف الـ Blueprint مع تحديث الاسم والمسار
# المسار الفعلي للقوالب سيكون: apps/suppliers_dashboard/templates/suppliers/
dashboard_bp = Blueprint('suppliers_dashboard', __name__, template_folder='templates')

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    """
    لوحة تحكم المورد (الجديدة)
    """
    # 1. التأكد من أن المستخدم الحالي هو مورد
    if not isinstance(current_user, Supplier):
        flash("غير مصرح لك بالوصول لهذه الصفحة", "danger")
        # تأكد أن اسم الـ Blueprint الخاص بالدخول هو 'suppliers'
        return redirect(url_for('suppliers.login'))
    
    # 2. إحصائيات افتراضية
    supplier_stats = {
        'total_sales': '0.00',
        'pending_orders': 0
    }
    
    # 3. عرض قالب الداشبورد المحدث
    # المسار المحدث: apps/suppliers_dashboard/templates/suppliers/dashboard.html
    return render_template('suppliers/dashboard.html', 
                           title="لوحة المورد", 
                           supplier_stats=supplier_stats)

@dashboard_bp.route('/')
@login_required
def index():
    """
    تحويل المسار الجذري للـ blueprint إلى لوحة التحكم
    """
    return redirect(url_for('suppliers_dashboard.dashboard'))
