# coding: utf-8
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
import traceback

# استيراد النماذج
from apps.models.admin_db import AdminUser
from apps.models.supplier_db import Supplier

# تأكد أن الـ template_folder يشير إلى مجلد templates الموجود داخل مجلد admin_dashboard
admin_dashboard = Blueprint('admin_dashboard', __name__, template_folder='templates')

@admin_dashboard.route('/dashboard')
@login_required
def dashboard():
    try:
        # فحص الصلاحية بشكل آمن (إذا كنت تواجه مشاكل استيراد، استخدم hasattr)
        if not getattr(current_user, 'is_admin', False) and not isinstance(current_user, AdminUser):
            return redirect(url_for('auth_portal.login'))

        total_suppliers = Supplier.query.count()
        
        return render_template(
            'admin/dashboard.html',
            total_suppliers=total_suppliers,
            total_balance_sar=0.0,
            total_balance_yer=0.0,
            total_balance_usd=0.0,
            recent_transactions=[]
        )
        
    except Exception as e:
        print(f"🚨 [CRITICAL ERROR] Dashboard failed: {traceback.format_exc()}")
        return "حدث خطأ فني أثناء تحميل لوحة التحكم", 500

@admin_dashboard.route('/suppliers')
@login_required
def manage_suppliers():
    if not isinstance(current_user, AdminUser):
        return redirect(url_for('auth_portal.login'))
        
    suppliers = Supplier.query.all()
    return render_template('admin/suppliers.html', suppliers=suppliers)
