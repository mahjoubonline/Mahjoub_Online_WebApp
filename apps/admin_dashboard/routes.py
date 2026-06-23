# coding: utf-8
# 📂 apps/admin_dashboard/routes.py - النسخة النهائية المستقرة

import os
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
import traceback

# استيراد النماذج
from apps.models.admin_db import AdminUser
from apps.models.supplier_db import Supplier

# الحل الجذري لمشكلة TemplateNotFound: 
# نحدد المسار المطلق لمجلد القوالب لضمان رؤية الخادم له في بيئة Render
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

admin_dashboard = Blueprint(
    'admin_dashboard', 
    __name__, 
    template_folder=template_dir
)

@admin_dashboard.route('/dashboard')
@login_required
def dashboard():
    """
    لوحة تحكم الإدارة المركزية
    """
    try:
        # فحص صلاحية الوصول للمدير
        if not getattr(current_user, 'is_admin', False) and not isinstance(current_user, AdminUser):
            flash("هذه المنطقة مخصصة للمدراء فقط.", "danger")
            return redirect(url_for('auth_portal.login'))

        total_suppliers = Supplier.query.count()
        
        # استدعاء القالب من المسار: templates/admin/dashboard.html
        return render_template(
            'admin/dashboard.html',
            total_suppliers=total_suppliers,
            total_balance_sar=0.0,
            total_balance_yer=0.0,
            total_balance_usd=0.0,
            recent_transactions=[]
        )
        
    except Exception as e:
        # تسجيل الخطأ في الـ Logs لتسهيل التتبع
        print(f"🚨 [CRITICAL ERROR] Dashboard failed: {traceback.format_exc()}")
        return "حدث خطأ فني أثناء تحميل لوحة التحكم، يرجى مراجعة سجلات الخادم.", 500

@admin_dashboard.route('/suppliers')
@login_required
def manage_suppliers():
    """
    عرض صفحة إدارة الموردين
    """
    if not isinstance(current_user, AdminUser):
        return redirect(url_for('auth_portal.login'))
        
    suppliers = Supplier.query.all()
    return render_template('admin/suppliers.html', suppliers=suppliers)
