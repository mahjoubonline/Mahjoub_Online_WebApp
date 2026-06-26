# coding: utf-8
# 📂 apps/auth_portal/routes.py

import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from apps.models.admin_db import AdminUser

# تعريف Blueprint - تم ربطه بملفات الـ templates في المجلد الخاص به
auth_portal = Blueprint(
    'auth_portal', 
    __name__, 
    template_folder='templates',
    url_prefix='/auth' # التوافق مع الـ Registry
)

# المسار السيادي للوحة التحكم (مخفي للخصوصية)
LOGIN_PATH = os.environ.get('ADMIN_LOGIN_PATH', '/m7jb_sovereign_hq_v2_99x')

@auth_portal.route(LOGIN_PATH, methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # البحث عن المسؤول
        admin = AdminUser.query.filter_by(username=username).first()
        
        # التحقق الأمني
        if admin and admin.check_password(password):
            login_user(admin) 
            flash('تم تسجيل الدخول بنجاح!', 'success')
            
            # توجيه إلى لوحة الإدارة المركزية
            return redirect(url_for('admin_dashboard.dashboard'))
        else:
            flash('بيانات الدخول غير صحيحة.', 'danger')
            
    return render_template('auth/login.html')

@auth_portal.route('/logout')
@login_required
def logout():
    logout_user()
    flash('تم تسجيل الخروج.', 'info')
    return redirect(url_for('auth_portal.login'))
