# coding: utf-8
# 📂 apps/vendor_dashboard/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from apps.models.supplier_db import Supplier

# تعريف الـ Blueprint
# نحدد template_folder='templates' ليعرف Flask أن القوالب داخل هذا المجلد
dashboard_bp = Blueprint('vendor_dashboard', __name__, template_folder='templates')

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    """
    لوحة تحكم المورد الرئيسية
    """
    # 1. التأكد من أن المستخدم الحالي هو مورد
    if not isinstance(current_user, Supplier):
        flash("غير مصرح لك بالوصول لهذه الصفحة", "danger")
        return redirect(url_for('vendors.login'))
    
    # 2. إحصائيات افتراضية (يمكنك ربطها بـ models لاحقاً)
    supplier_stats = {
        'total_sales': '0.00',
        'pending_orders': 0
    }
    
    # 3. عرض قالب الداشبورد
    # المسار الفعلي سيكون: apps/vendor_dashboard/templates/vendor/dashboard.html
    return render_template('vendor/dashboard.html', 
                           title="لوحة المورد", 
                           supplier_stats=supplier_stats)

@dashboard_bp.route('/')
@login_required
def index():
    """
    تحويل المسار الجذري للـ blueprint إلى لوحة التحكم
    """
    return redirect(url_for('vendor_dashboard.dashboard'))
