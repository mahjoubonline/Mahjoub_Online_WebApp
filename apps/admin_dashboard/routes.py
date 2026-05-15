# coding: utf-8
# 📊 وحدة القيادة المركزية - محجوب أونلاين 2026
# التوثيق: إدارة لوحة التحكم وحوكمة عرض البيانات السيادية

from flask import render_template
from flask_login import login_required, current_user # حماية المنطقة السيادية
from . import admin_dashboard 

@admin_dashboard.route('/')
@admin_dashboard.route('/dashboard')
@login_required # درع أمني: النفاذ فقط للمصرح لهم بعد تسجيل الدخول
def dashboard():
    """
    عرض مركز المراقبة الرئيسي.
    يتم حقن dashboard_content.html داخل الإطار الملكي admin_base.html
    """
    # إحصائيات أولية للمنصة (سيتم ربطها بقاعدة البيانات لاحقاً)
    stats = {
        'total_suppliers': 0,
        'active_orders': 0,
        'system_health': '100%',
        'server_status': 'Online'
    }
    
    # تمرير كائن 'current_user' ليعرف النظام أنك المالك 'Owner'
    return render_template('admin/dashboard_content.html', stats=stats, owner=current_user)

@admin_dashboard.route('/suppliers/list')
@login_required
def list_suppliers():
    """
    عرض سجل الموردين المعتمدين في المنظومة.
    المسار: apps/templates/admin/list_suppliers.html
    """
    # سيتم جلب قائمة الموردين من قاعدة البيانات هنا مستقبلاً
    # suppliers = Supplier.query.all()
    return render_template('admin/list_suppliers.html', owner=current_user)

@admin_dashboard.route('/settings')
@login_required
def system_settings():
    """
    إعدادات السيادة والحوكمة للمنصة.
    """
    return render_template('admin/settings.html', owner=current_user)
