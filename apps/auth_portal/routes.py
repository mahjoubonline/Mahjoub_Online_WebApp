# coding: utf-8
# 📂 apps/auth_portal/routes.py

import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from flask_login import login_user, logout_user, current_user
from apps.models.admin_db import AdminUser

# تعريف الـ Blueprint
auth_portal = Blueprint(
    'auth_portal', 
    __name__, 
    template_folder='templates'
)

# الرابط السري للإدارة من المتغيرات البيئية
LOGIN_PATH = os.environ.get('ADMIN_LOGIN_PATH', '/m7jb_sovereign_hq_v2_99x')

@auth_portal.route(LOGIN_PATH, methods=['GET', 'POST'])
def login():
    """بوابة دخول الإدارة مع معالجة آمنة للمسارات."""
    
    # 1. التحقق من وجود جلسة فعالة
    if current_user.is_authenticated and session.get('user_type') == 'admin':
        return redirect(url_for('admin_dashboard.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # البحث في قاعدة بيانات المدراء
        admin = AdminUser.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password):
            login_user(admin, remember=True)
            session['user_type'] = 'admin' 
            
            flash('مرحباً بك يا مدير النظام.', 'success')
            
            # محاولة التحويل إلى الدوشبورد مع التقاط الأخطاء
            try:
                return redirect(url_for('admin_dashboard.dashboard'))
            except Exception as e:
                current_app.logger.error(f"Error redirecting to dashboard: {e}")
                flash('خطأ في تحديد مسار لوحة التحكم، يرجى التواصل مع الدعم التقني.', 'danger')
                return redirect(url_for('auth_portal.login'))
        else:
            flash('بيانات دخول غير صحيحة.', 'danger')
            
    return render_template('auth/login.html')

@auth_portal.route('/logout')
def logout():
    """تسجيل الخروج مع مسح شامل للجلسة لمنع تداخل الصلاحيات."""
    logout_user()
    session.clear() 
    flash('تم تسجيل الخروج بنجاح.', 'info')
    return redirect(url_for('auth_portal.login'))
