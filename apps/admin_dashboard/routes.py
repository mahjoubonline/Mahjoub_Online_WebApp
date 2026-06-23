# coding: utf-8
# 📂 apps/admin_dashboard/routes.py - النسخة النهائية الموثوقة

import os
import traceback
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

# استيراد النماذج
from apps.models.admin_db import AdminUser
from apps.models.supplier_db import Supplier

# تعريف الـ Blueprint
# نحدد template_folder='templates' لكي يبحث Flask عن القوالب داخل مجلد templates الخاص بهذا المجلد
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
        # فحص صلاحية الوصول: التأكد أن المستخدم مدير (Admin)
        if not getattr(current_user, 'is_admin', False) and not isinstance(current_user, AdminUser):
            flash("عذراً، هذه المنطقة مخصصة للمدراء فقط.", "danger")
            return redirect(url_for('auth_portal.login'))

        # جلب البيانات الأساسية
        total_suppliers = Supplier.query.count()
        
        # عند استخدام template_folder='templates'، يبدأ البحث من داخل المجلد المسمى 'templates'.
        # إذا كان مسار ملفك هو: apps/admin_dashboard/templates/admin/dashboard.html
        # فإن الطلب الصحيح هو 'admin/dashboard.html'
        return render_template(
            'admin/dashboard.html',
            total_suppliers=total_suppliers,
            total_balance_sar=0.0,
            total_balance_yer=0.0,
            total_balance_usd=0.0,
            recent_transactions=[]
        )
        
    except Exception as e:
        # طباعة الخطأ الكامل في الـ Logs لتسهيل التصحيح ومعرفة سبب فشل العثور على القالب
        print(f"🚨 [CRITICAL ERROR] Template Loading Failed: {traceback.format_exc()}")
        return f"حدث خطأ فني في تحميل الواجهة: {str(e)}", 500

@admin_dashboard.route('/suppliers')
@login_required
def manage_suppliers():
    """عرض قائمة الموردين"""
    # فحص صلاحية الوصول
    if not isinstance(current_user, AdminUser):
        return redirect(url_for('auth_portal.login'))
        
    try:
        suppliers = Supplier.query.all()
        # المسار الفعلي: templates/admin/suppliers.html
        return render_template('admin/suppliers.html', suppliers=suppliers)
    except Exception as e:
        print(f"🚨 [CRITICAL ERROR] Suppliers Page Failed: {traceback.format_exc()}")
        return "حدث خطأ في تحميل قائمة الموردين", 500
