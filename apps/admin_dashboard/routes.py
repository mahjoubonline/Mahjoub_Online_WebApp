# coding: utf-8
# 📂 apps/admin_dashboard/routes.py - النسخة النهائية المطابقة للهيكلية

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
import traceback

from apps.models.admin_db import AdminUser
from apps.models.supplier_db import Supplier

# تأكد أن المجلد هو templates/ مباشرة
admin_dashboard = Blueprint('admin_dashboard', __name__, template_folder='templates')

@admin_dashboard.route('/dashboard')
@login_required
def dashboard():
    try:
        if not isinstance(current_user, AdminUser):
            return redirect(url_for('auth_portal.login'))

        total_suppliers = Supplier.query.count()
        
        # تمرير المتغيرات المطلوبة في القالب
        return render_template(
            'admin/dashboard.html',
            total_suppliers=total_suppliers,
            total_balance_sar=0.0,
            total_balance_yer=0.0,
            total_balance_usd=0.0,
            recent_transactions=[]
        )
        
    except Exception as e:
        # هذا سيطبع المسار المسبب للخطأ بالضبط في الـ Logs
        print(f"🚨 [CRITICAL ERROR] {traceback.format_exc()}")
        return f"حدث خطأ في تحميل الصفحة: {str(e)}", 500

@admin_dashboard.route('/suppliers')
@login_required
def manage_suppliers():
    if not isinstance(current_user, AdminUser):
        return redirect(url_for('auth_portal.login'))
    suppliers = Supplier.query.all()
    return render_template('admin/suppliers.html', suppliers=suppliers)
