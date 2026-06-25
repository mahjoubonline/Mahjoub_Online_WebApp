# coding: utf-8
# 📂 apps/suppliers_dashboard/routes.py

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
# تأكد من استيراد الموديلات اللازمة إذا كنت ستستخدمها هنا
# from apps.models.supplier_db import Supplier 

# تعريف الـ Blueprint مع تحديد مسار الـ templates بدقة
dashboard_bp = Blueprint('suppliers_dashboard', __name__, template_folder='templates')

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    """
    لوحة تحكم المورد - عرض البيانات الحقيقية من قاعدة البيانات
    """
    # حساب الطلبات قيد التنفيذ
    pending_orders_count = 0
    if hasattr(current_user, 'orders') and current_user.orders:
        pending_orders_count = len([o for o in current_user.orders if o.status == 'pending'])
    
    # حساب إجمالي المبيعات المكتملة
    total_sales = 0.00
    if hasattr(current_user, 'financials') and current_user.financials:
        total_sales = sum(float(f.amount) for f in current_user.financials if f.status == 'completed')

    # إعداد الإحصائيات للواجهة
    supplier_stats = {
        'total_sales': "{:,.2f}".format(total_sales),
        'pending_orders': pending_orders_count
    }
    
    # render_template سيتعرف على المجلد الفرعي 'suppliers/' داخل templates
    return render_template('suppliers/dashboard.html', 
                           supplier_stats=supplier_stats)

@dashboard_bp.route('/')
@login_required
def index():
    """
    تحويل المسار الجذري للـ blueprint إلى لوحة التحكم
    """
    return redirect(url_for('suppliers_dashboard.dashboard'))
