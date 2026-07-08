# coding: utf-8
# 📂 apps/admin_permissions/routes.py

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from apps.models import db, Role

# تعريف الـ Blueprint مع تحديد مسار القوالب
admin_permissions_bp = Blueprint(
    'admin_permissions', 
    __name__, 
    template_folder='templates'
)

# دالة للتحقق من صلاحية المدير (يمكنك ربطها بنظام الصلاحيات لاحقاً)
def is_admin():
    # التحقق من أن المستخدم مسجل وله صلاحية الإدارة
    return current_user.is_authenticated and (getattr(current_user, 'role', '') == 'admin' or getattr(current_user, 'role', '') == 'Owner')

@admin_permissions_bp.route('/admin/permissions/roles', methods=['GET'])
@login_required
def roles_list():
    """عرض قائمة الأدوار المتاحة في النظام."""
    if not is_admin():
        flash("عذراً، غير مصرح لك بالدخول إلى هذه الصفحة.", "danger")
        return redirect(url_for('admin_dashboard.dashboard'))
    
    # جلب الأدوار من قاعدة البيانات المركزية
    roles = Role.query.all()
    return render_template('admin/permissions.html', roles=roles, active_tab='roles')

@admin_permissions_bp.route('/admin/permissions/assign', methods=['GET', 'POST'])
@login_required
def assign_permissions():
    """صفحة إسناد الصلاحيات للمستخدمين."""
    if not is_admin():
        flash("عذراً، غير مصرح لك بالدخول إلى هذه الصفحة.", "danger")
        return redirect(url_for('admin_dashboard.dashboard'))
    
    # منطق الإسناد سيتم بناؤه هنا لاحقاً
    return render_template('admin/permissions.html', active_tab='assign')
