# coding: utf-8
# 📂 apps/admin_dashboard/routes.py - النسخة النهائية الموثوقة

import traceback
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

# استيراد النماذج
from apps.models.admin_db import AdminUser
from apps.models.supplier_db import Supplier

# تعريف الـ Blueprint
# المسار هنا يعتمد على أن الـ templates موجودة في مجلد templates الخاص بهذا المجلد
admin_dashboard = Blueprint(
    'admin_dashboard', 
    __name__, 
    template_folder='templates'
)

@admin_dashboard.route('/dashboard')
@login_required
def dashboard():
    """لوحة تحكم الإدارة المركزية"""
    try:
        # فحص صلاحية الوصول
        if not getattr(current_user, 'is_admin', False) and not isinstance(current_user, AdminUser):
            flash("عذراً، هذه المنطقة مخصصة للمدراء فقط.", "danger")
            return redirect(url_for('auth_portal.login'))

        # جلب البيانات
        total_suppliers = Supplier.query.count()
        
        # تصحيح: استدعاء القالب باسمه الحقيقي الموجود في المسار:
        # apps/admin_dashboard/templates/admin/dashboard_content.html
        return render_template(
            'admin/dashboard_content.html',
            total_suppliers=total_suppliers,
            total_balance_sar=0.0,
            total_balance_yer=0.0,
            total_balance_usd=0.0,
            recent_transactions=[]
        )
        
    except Exception as e:
        print(f"🚨 [CRITICAL ERROR] Template Loading Failed: {traceback.format_exc()}")
        return f"حدث خطأ فني في تحميل الواجهة: {str(e)}", 500

@admin_dashboard.route('/suppliers')
@login_required
def manage_suppliers():
    """عرض قائمة الموردين"""
    if not isinstance(current_user, AdminUser):
        return redirect(url_for('auth_portal.login'))
        
    try:
        suppliers = Supplier.query.all()
        # تأكد من وجود ملف suppliers.html في نفس مسار admin_base.html
        return render_template('admin/suppliers.html', suppliers=suppliers)
    except Exception as e:
        print(f"🚨 [CRITICAL ERROR] Suppliers Page Failed: {traceback.format_exc()}")
        return "حدث خطأ في تحميل قائمة الموردين", 500
