# coding: utf-8
# 📂 apps/auth_portal/routes.py - النسخة المباشرة (بدون تحقق OTP)

import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user
from apps.models.admin_db import AdminUser

# إنشاء Blueprint للـ Auth Portal
auth_portal = Blueprint('auth_portal', __name__, template_folder='templates')

# المسار الديناميكي
LOGIN_PATH = os.environ.get('ADMIN_LOGIN_PATH', '/m7jb_sovereign_hq_v2_99x')

@auth_portal.route(LOGIN_PATH, methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # البحث عن المستخدم في قاعدة البيانات
        admin = AdminUser.query.filter_by(username=username).first()
        
        # التحقق من كلمة المرور
        if admin and admin.check_password(password):
            # تسجيل الدخول مباشرة بدون الحاجة لـ OTP
            login_user(admin) 
            flash('تم تسجيل الدخول بنجاح!', 'success')
            return redirect(url_for('admin_dashboard.index'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة.', 'danger')
            
    return render_template('auth/login.html')

# تمت إزالة مسار /verify-otp بالكامل لأنه لم يعد له حاجة
