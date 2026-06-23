# coding: utf-8
# 📂 apps/admin_dashboard/routes.py - لوحة تحكم الإدارة المركزية (مُحسنة)

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
import traceback

# استيراد النماذج
from apps.models.admin_db import AdminUser
from apps.models.supplier_db import Supplier

admin_dashboard = Blueprint('admin_dashboard', __name__, template_folder='templates')

@admin_dashboard.route('/dashboard')
@login_required
def dashboard():
    """
    لوحة تحكم القيادة المركزية للمدير
    """
    try:
        # 1. حماية سيادية: التحقق باستخدام معرف فريد في جدول الإدارة
        # بدلاً من isinstance التي قد تفشل بسبب Circular Import
        if not hasattr(current_user, 'is_admin') or not current_user.is_admin:
            # ملاحظة: تأكد أن نموذج AdminUser يحتوي على خاصية is_admin=True
            # إذا لم تكن موجودة، استخدم التحقق عبر البريد أو النوع
            if not isinstance(current_user, AdminUser):
                flash("هذه المنطقة مخصصة للمدراء فقط.", "danger")
                return redirect(url_for('auth_portal.login'))

        # 2. جلب إحصائيات النظام
        total_suppliers = Supplier.query.count()
        
        stats = {
            'total_suppliers': total_suppliers,
            'active_orders': 0,
            'central_balance': "0.00"
        }
        
        return render_template('admin/dashboard.html', stats=stats)
        
    except Exception as e:
        # 💡 طباعة الخطأ الحقيقي بالتفصيل في الـ Logs لتسهيل التصحيح
        print(f"🚨 [CRITICAL ERROR] Dashboard failed: {traceback.format_exc()}")
        return f"حدث خطأ فني أثناء تحميل لوحة التحكم: {str(e)}", 500

@admin_dashboard.route('/suppliers')
@login_required
def manage_suppliers():
    """عرض قائمة الموردين للمدير"""
    if not isinstance(current_user, AdminUser):
        return redirect(url_for('auth_portal.login'))
        
    suppliers = Supplier.query.all()
    return render_template('admin/suppliers.html', suppliers=suppliers)
