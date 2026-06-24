# coding: utf-8
# 📂 apps/auth_portal/routes.py - بوابة الدخول السيادية (النسخة النهائية المؤكدة)

import random
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from apps.auth_portal.auth_service import AdminAuthService
from apps.models.admin_db import AdminUser

# تعريف الـ Blueprint
auth_portal = Blueprint('auth_portal', __name__, template_folder='templates')

@auth_portal.route('/m7jb_sovereign_hq_v2_99x', methods=['GET', 'POST'])
def login():
    """
    المرحلة 1: استقبال الهوية، البحث عنها في القاعدة، وإرسال الرمز.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        
        # البحث عن المسؤول في القاعدة
        admin = AdminUser.query.filter_by(username=username).first()
        
        if admin and admin.phone_number:
            # توليد رمز عشوائي
            otp_code = str(random.randint(100000, 999999))
            
            # محاولة الإرسال
            if AdminAuthService.initiate_login(admin.phone_number, otp_code):
                session['otp_code'] = otp_code
                session['user_id'] = admin.id
                return redirect(url_for('auth_portal.verify_otp_page'))
            else:
                flash("فشل الاتصال بخدمة الإرسال، حاول لاحقاً.")
        else:
            flash("هوية غير معروفة أو لا يوجد رقم هاتف مرتبط.")
            
    return render_template('auth/login.html')

@auth_portal.route('/verify', methods=['GET', 'POST'])
def verify_otp_page():
    """
    المرحلة 2: التحقق من الرمز والانتهاء من الدخول.
    """
    if 'otp_code' not in session:
        return redirect(url_for('auth_portal.login'))

    if request.method == 'POST':
        user_otp = request.form.get('otp_code')
        
        if user_otp == session.get('otp_code'):
            # نجاح التحقق - هنا يمكنك إضافة كود تسجيل الدخول (login_user)
            session.pop('otp_code', None)
            return "✅ تم الدخول بنجاح إلى النظام السيادي."
        else:
            flash("رمز التحقق غير صحيح.")
            
    return render_template('auth/verify_otp.html')

@auth_portal.route('/resend', methods=['POST'])
def resend_otp():
    """إعادة إرسال الرمز"""
    user_id = session.get('user_id')
    admin = AdminUser.query.get(user_id) if user_id else None
    
    if admin:
        new_otp = str(random.randint(100000, 999999))
        if AdminAuthService.initiate_login(admin.phone_number, new_otp):
            session['otp_code'] = new_otp
            flash("تمت إعادة إرسال الرمز.")
    return redirect(url_for('auth_portal.verify_otp_page'))
