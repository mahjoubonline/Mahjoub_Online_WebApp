# coding: utf-8
# 📂 apps/auth_portal/routes.py - النسخة المصححة والمطابقة للرابط المطلوب

import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from apps.auth_portal.auth_service import AdminAuthService
from apps.models.admin_db import AdminUser
import random

# إنشاء Blueprint للـ Auth Portal
auth_portal = Blueprint('auth_portal', __name__, template_folder='templates')

# تعديل المسار ليطابق الرابط الذي يطلبه السيرفر: /auth/m7jb_sovereign_hq_v2_99x
# ملاحظة: بما أن الـ Blueprint مسجل بـ /auth، المسار هنا يجب أن يبدأ بـ /m7jb...
LOGIN_PATH = os.environ.get('ADMIN_LOGIN_PATH', '/m7jb_sovereign_hq_v2_99x')

@auth_portal.route(LOGIN_PATH, methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = AdminUser.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password):
            otp_code = str(random.randint(100000, 999999))
            session['otp_code'] = otp_code
            session['phone'] = admin.phone_number
            
            if AdminAuthService.initiate_login(admin.phone_number, otp_code):
                flash('تم إرسال رمز التحقق إلى واتساب الخاص بك.', 'success')
                return redirect(url_for('auth_portal.verify_otp'))
            else:
                flash('حدث خطأ أثناء إرسال الرمز. يرجى المحاولة لاحقاً.', 'danger')
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة.', 'danger')
            
    return render_template('auth/login.html')

@auth_portal.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if 'otp_code' not in session:
        return redirect(url_for('auth_portal.login'))

    if request.method == 'POST':
        user_otp = request.form.get('otp_code')
        
        if user_otp == session.get('otp_code'):
            session.pop('otp_code', None)
            session.pop('phone', None)
            flash('تم تسجيل الدخول بنجاح!', 'success')
            return redirect(url_for('admin_dashboard.index')) # تأكد أن هذا هو اسم الدالة الصحيح في admin_dashboard
        else:
            flash('الرمز غير صحيح، حاول مرة أخرى.', 'danger')
            
    return render_template('auth/verify_otp.html')
