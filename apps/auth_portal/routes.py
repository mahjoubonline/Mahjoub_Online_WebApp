from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.admin_db import AdminUser 

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_input = request.form.get('username')
        password_input = request.form.get('password')

        # 1. البحث عن المستخدم في جدول admin_users
        user = AdminUser.query.filter_by(username=username_input).first()

        if user:
            # 2. التحقق من التشفير
            if user.check_password(password_input):
                session['user_id'] = user.id
                session['username'] = user.username
                session['role'] = user.role 
                
                flash(f'مرحباً بك يا {user.full_name}، تم توثيق الدخول بنجاح', 'success')
                
                # --- الإصلاح الجوهري هنا ---
                # نقوم بالتوجيه إلى الـ dashboard بدلاً من add_supplier
                try:
                    return redirect(url_for('admin_dashboard.dashboard'))
                except:
                    # مسار احتياطي في حال وجود مشكلة في تسمية الـ Blueprint
                    return redirect('/admin/dashboard')
            else:
                flash('خطأ: كلمة المرور غير مطابقة للسجلات المشفرة.', 'danger')
        else:
            flash('تنبيه: هذا المستخدم غير معرف في المنظومة.', 'warning')
            
        return redirect(url_for('auth.login'))

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('تم تسجيل الخروج من المنظومة بنجاح.', 'info')
    return redirect(url_for('auth.login'))
