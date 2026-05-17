# coding: utf-8
# 📊 وحدة القيادة المركزية - محجوب أونلاين 2026

from flask import render_template, current_app
from flask_login import login_required, current_user 
import jinja2

# استيراد البلوبرينت الموحد لمنع تعذر العثور على الكائن أثناء الإقلاع
from . import admin_dashboard_blueprint 


@admin_dashboard_blueprint.route('/')
@admin_dashboard_blueprint.route('/dashboard')
@login_required # درع حماية النفاذ السيادي
def dashboard_home():
    """
    عرض مركز المراقبة الرئيسي.
    يتم رندرة القالب المخصص للوحة التحكم مع معالجة استثنائية للمسارات المعزولة.
    """
    stats = {
        'total_suppliers': 0,
        'active_orders': 0,
        'system_health': '100%',
        'server_status': 'Online'
    }
    
    # محاولة رندرة القالب بالمسار المعزول، وإذا تعذر يتم البحث عنه في المسار المباشر منعا للانهيار
    try:
        return render_template('admin/dashboard_content.html', stats=stats, owner=current_user)
    except jinja2.exceptions.TemplateNotFound:
        current_app.logger.warning("تنبيه: تم موازنة مسار القالب المعزول لـ dashboard_content")
        return render_template('dashboard_content.html', stats=stats, owner=current_user)


@admin_dashboard_blueprint.route('/suppliers/list')
@login_required
def list_suppliers():
    """عرض سجل الموردين"""
    try:
        return render_template('admin/list_suppliers.html', owner=current_user)
    except jinja2.exceptions.TemplateNotFound:
        return render_template('list_suppliers.html', owner=current_user)


@admin_dashboard_blueprint.route('/settings')
@login_required
def system_settings():
    """إعدادات المنصة السيادية"""
    try:
        return render_template('admin/settings.html', owner=current_user)
    except jinja2.exceptions.TemplateNotFound:
        return render_template('settings.html', owner=current_user)
