# coding: utf-8
# 📂 apps/auth_portal/routes.py - مسارات المصادقة المحصنة بالتأمين السيادي

import os
import time
import random
from flask import render_template, request, redirect, url_for, flash, abort, session
from flask_login import login_user, logout_user, login_required, current_user
from apps.extensions import db
from . import auth_blueprint
from apps.models.admin_db import AdminUser

# مسار الدخول السري (يُجلب من إعدادات البيئة)
SECRET_LOGIN_PATH = os.environ.get('ADMIN_LOGIN_PATH', '/gatekeeper_secure_entry_2026')

# -------------------------------------------------------------------------
# 1. المسار السري (Login) - مع المحرك الأمني للتأخير العشوائي
# -------------------------------------------------------------------------
@auth_blueprint.route(SECRET_LOGIN_PATH, methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard.dashboard'))

    if request.method == 'POST':
        username = str(request.form.get('username', '')).strip()
        password = request.form.get('password', '')
        
        # محرك أمني: تأخير زمني وهمي لمنع هجمات التخمين الآلية
        time.sleep(random.uniform(0.6, 1.2))
        
        user = AdminUser.query.filter_by(username=username).first()
        error_msg = 'بيانات الدخول غير صحيحة.'

        if user and user.check_password(password):
            if user.is_locked():
                flash('الحساب مقفل مؤقتاً. يرجى الانتظار.', 'danger')
            elif user.role in ['Owner', 'Admin']:
                session['pending_user_id'] = user.id
                return redirect(url_for('auth_blueprint.verify_otp'))
            else:
                flash(error_msg, 'danger')
        else:
            if user:
                user.increment_failed_attempts()
            flash(error_msg, 'danger')
    
    return render_template('auth/login.html')

# -------------------------------------------------------------------------
# 2. نظام التحقق الثنائي (2FA) - محصن ومربوط بقاعدة البيانات
# -------------------------------------------------------------------------
@auth_blueprint.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    user_id = session.get('pending_user_id')
    if not user_id:
        return redirect(url_for('auth_blueprint.login'))
    
    user = AdminUser.query.get(user_id)
    
    if user.is_locked():
        flash('تم قفل الحساب مؤقتاً بسبب كثرة المحاولات.', 'danger')
        return render_template('auth/verify_otp.html')

    if request.method == 'POST':
        otp = request.form.get('otp')
        if user.verify_otp_code(otp):
            login_user(user)
            session.pop('pending_user_id', None)
            user.reset_failed_attempts()
            return redirect(url_for('admin_dashboard.dashboard'))
        else:
            user.increment_failed_attempts()
            flash('كود التحقق غير صحيح.', 'danger')

    return render_template('auth/verify_otp.html')

# -------------------------------------------------------------------------
# 3. مسارات الطوارئ (تمويه وإدارة)
# -------------------------------------------------------------------------
@auth_blueprint.route('/resend-otp')
def resend_otp():
    user_id = session.get('pending_user_id')
    if user_id:
        # استدعاء خدمة الواتساب السيادية لاحقاً
        flash('تم إرسال كود جديد عبر واتساب.', 'info')
    return redirect(url_for('auth_blueprint.verify_otp'))

@auth_blueprint.route('/upload-identity', methods=['GET', 'POST'])
def upload_identity():
    return render_template('auth/upload_id.html')

# -------------------------------------------------------------------------
# 4. مسار الكمين (Decoy) - لخداع البوتات
# -------------------------------------------------------------------------
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def decoy_login():
    abort(404)

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_blueprint.login'))
