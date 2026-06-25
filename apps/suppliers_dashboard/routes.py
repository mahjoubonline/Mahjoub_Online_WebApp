# coding: utf-8
# 📂 apps/suppliers_dashboard/routes.py

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from apps.models.supplier_db import Supplier

# تعريف الـ Blueprint
dashboard_bp = Blueprint('suppliers_dashboard', __name__, template_folder='templates')

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    """
    لوحة تحكم المورد - عرض البيانات الحقيقية من قاعدة البيانات
    """
    # حساب الطلبات قيد التنفيذ من خلال العلاقة التي عرفناها في الموديل
    pending_orders_count = 0
    if current_user.orders:
        pending_orders_count = len([o for o in current_user.orders if o.status == 'pending'])
    
    # حساب المبيعات (مثال: مجموع القيم المالية للطلبات المكتملة)
    total_sales = 0.00
    if current_user.financials:
        total_sales = sum(float(f.amount) for f in current_user.financials if f.status == 'completed')

    # إعداد الإحصائيات للواجهة
    supplier_stats = {
        'total_sales': "{:,.2f}".format(total_sales),
        'pending_orders': pending_orders_count
    }
    
    # تمرير current_user تلقائياً للـ template عبر Flask-Login
    return render_template('suppliers/dashboard.html', 
                           supplier_stats=supplier_stats)

@dashboard_bp.route('/')
@login_required
def index():
    """
    تحويل المسار الجذري للـ blueprint إلى لوحة التحكم
    """
    return redirect(url_for('suppliers_dashboard.dashboard'))
