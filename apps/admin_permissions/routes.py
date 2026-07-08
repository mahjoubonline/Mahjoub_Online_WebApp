# coding: utf-8
# 📂 apps/admin_permissions/routes.py

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from apps.models import db, Role  # سنستخدم نماذجك المركزية

# تعريف الـ Blueprint
admin_permissions_bp = Blueprint(
    'admin_permissions', 
    __name__, 
    template_folder='templates'
)

# دالة مساعدة للتحقق من صلاحية المدير (يمكن تطويرها لاحقاً)
def is_admin():
    return current_user.is_authenticated and current_user.role == 'admin'

@admin_permissions_bp.route('/admin/permissions/roles', methods=['GET'])
@login_required
def roles_list():
    if not is_admin():
        flash("غير مصرح لك بالدخول", "danger")
        return redirect(url_for('admin_dashboard.dashboard'))
    
    # جلب الأدوار من قاعدة البيانات المركزية
    roles = Role.query.all()
    return render_template('admin/permissions.html', roles=roles, active_tab='roles')

@admin_permissions_bp.route('/admin/permissions/assign', methods=['GET', 'POST'])
@login_required
def assign_permissions():
    if not is_admin():
        flash("غير مصرح لك بالدخول", "danger")
        return redirect(url_for('admin_dashboard.dashboard'))
    
    # هنا سنضيف منطق إسناد الصلاحيات للمستخدمين
    return render_template('admin/permissions.html', active_tab='assign')
