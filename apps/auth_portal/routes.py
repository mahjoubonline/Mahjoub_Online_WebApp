# coding: utf-8
# 📂 apps/auth_portal/routes.py - بوابة الدخول السيادية (النسخة المحصنة)

import random
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from apps.auth_portal.auth_service import AdminAuthService
from apps.models.admin_db import AdminUser

auth_portal = Blueprint('auth_portal', __name__, template_folder='templates')

@auth_portal.route('/m7jb_sovereign_hq_v2_99x', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = AdminUser.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password):
            # إخلاء أي جلسة سابقة قبل البدء
            session.clear() 
            
            otp_code = str(random.randint(100000, 999999))
            
            if AdminAuthService.initiate_login(admin.phone_number, otp_code):
                session['otp_code'] = otp_code
                session['user_id'] = admin.id
                session['login_attempts'] = 0 # تعقب المحاولات
                return redirect(url_for('auth_portal.verify_otp_page'))
            else:
                flash("فشل الاتصال بخدمة الإرسال، حاول لاحقاً.")
        else:
            flash("اسم المستخدم أو كلمة المرور غير صحيحة.")
            
    return render_template('auth/login.html')

@auth_portal.route('/verify', methods=['GET', 'POST'])
def verify_otp_page():
    if 'otp_code' not in session:
        return redirect(url_for('auth_portal.login'))

    if request.method == 'POST':
        user_otp = request.form.get('otp_code')
        
        # حماية ضد المحاولات المتكررة (تسمح بـ 3 محاولات فقط)
        session['login_attempts'] = session.get('login_attempts', 0) + 1
        if session['login_attempts'] > 3:
            session.clear()
            flash("تم تجاوز عدد المحاولات المسموح بها، يرجى إعادة تسجيل الدخول.")
            return redirect(url_for('auth_portal.login'))
        
        if user_otp == session.get('otp_code'):
            session.pop('otp_code', None)
            session.pop('login_attempts', None)
            return "✅ تم الدخول بنجاح إلى النظام السيادي."
        else:
            flash(f"رمز التحقق غير صحيح. محاولات متبقية: {3 - session['login_attempts']}")
            
    return render_template('auth/verify_otp.html')

@auth_portal.route('/resend', methods=['POST'])
def resend_otp():
    user_id = session.get('user_id')
    admin = AdminUser.query.get(user_id) if user_id else None
    
    if admin:
        new_otp = str(random.randint(100000, 999999))
        if AdminAuthService.initiate_login(admin.phone_number, new_otp):
            session['otp_code'] = new_otp
            flash("تمت إعادة إرسال الرمز.")
        else:
            flash("فشل إعادة الإرسال.")
            
    return redirect(url_for('auth_portal.verify_otp_page'))
