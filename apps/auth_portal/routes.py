from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.admin_db import AdminUser  # استيراد الموديل للتحقق من القاعدة

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 1. محاولة الدخول عبر قاعدة البيانات (للمسؤولين المسجلين)
        user = AdminUser.query.filter_by(username=username).first()
        
        # إذا وجد المستخدم وكانت كلمة السر صحيحة (مشفرة)
        if user and user.check_password(password):
            session['is_authenticated'] = True
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('admin.dashboard'))

        # 2. دخول الطوارئ للمؤسس (علي محجوب) - لضمان الدخول حتى لو القاعدة فارغة
        elif username == 'ali_mahjoub' and password == '123':
            session['is_authenticated'] = True
            session['user_id'] = 'founder_ali'
            session['username'] = 'علي محجوب'
            return redirect(url_for('admin.dashboard'))
            
        else:
            flash('بيانات الدخول غير صحيحة يا قائد، حاول مرة أخرى.', 'danger')
            
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
