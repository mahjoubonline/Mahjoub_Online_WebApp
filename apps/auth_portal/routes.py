from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.admin_db import AdminUser  # استيراد نموذج المستخدمين

# ملاحظة: تأكد أن الاسم 'auth' يطابق ما استخدمناه في run.py (url_for('auth.login'))
auth_bp = Blueprint(
    'auth', 
    __name__, 
    template_folder='templates'
)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_input = request.form.get('username')
        password_input = request.form.get('password')

        # 1. البحث عن المستخدم في قاعدة البيانات
        user = AdminUser.query.filter_by(username=username_input).first()

        if user:
            # 2. التحقق من كلمة المرور
            # ملاحظة: إذا كنت تستخدم التشفير، استبدل المقارنة بـ check_password_hash
            if user.password == password_input:
                session['user_id'] = user.id
                session['username'] = user.username
                
                flash(f'مرحباً بك مجدداً يا {user.username} في منظومة محجوب', 'success')
                # التوجه إلى لوحة التحكم الإدارية
                return redirect(url_for('admin.index')) # تأكد من اسم الـ Blueprint للوحة التحكم
            else:
                # كلمة السر خاطئة
                flash('خطأ سيادي: كلمة المرور التي أدخلتها غير صحيحة.', 'danger')
        else:
            # المستخدم غير موجود أصلاً
            flash('تنبيه: اسم المستخدم هذا غير مسجل في سجلات المنظومة.', 'warning')
            
        return redirect(url_for('auth.login'))

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('تم إنهاء الجلسة وتأمين الخروج بنجاح.', 'info')
    return redirect(url_for('auth.login'))
