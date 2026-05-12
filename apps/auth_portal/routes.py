from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.admin_db import AdminUser, db

# تعريف الـ Blueprint
auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # سحب البيانات من الحقول (يجب أن تطابق الـ name في HTML)
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 1. التحقق المباشر (دخول الطوارئ الخاص بعلي محجوب)
        if username == 'ali_mahjoub' and password == '123':
            session.clear()
            session['is_authenticated'] = True
            session['user_id'] = 'founder_ali'
            session['username'] = 'علي محجوب'
            return redirect(url_for('admin.dashboard'))

        # 2. التحقق عبر قاعدة البيانات (إذا تم تفعيل التشفير لاحقاً)
        try:
            user = AdminUser.query.filter_by(username=username).first()
            if user and user.check_password(password):
                session.clear()
                session['is_authenticated'] = True
                session['user_id'] = user.id
                return redirect(url_for('admin.dashboard'))
        except Exception as e:
            # في حال لم يكن الجدول موجوداً بعد
            pass
        
        # رسالة الخطأ
        flash('بيانات الدخول غير صحيحة، يرجى التأكد من اسم المستخدم وكلمة المرور.', 'danger')
            
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
