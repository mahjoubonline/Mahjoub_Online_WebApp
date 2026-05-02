from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from core.models.user import User  # استدعاء موديل القائد من القلب المركزي
from . import admin_bp  # استدعاء Blueprint الإدارة

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    """منطق تسجيل دخول القائد إلى لوحة التحكم"""
    
    # إذا كان القائد مسجلاً دخوله بالفعل، يتم توجيهه للوحة التحكم مباشرة
    if current_user.is_authenticated:
        return redirect(url_for('admin.admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # البحث عن المستخدم "علي محجوب" في القاعدة التي تم تصفيتها
        user = User.query.filter_by(username=username).first()
        
        # التحقق من الهوية وكلمة السر (123)
        if user and user.check_password(password):
            login_user(user)
            flash('أهلاً بك يا قائد، تم الدخول بنجاح.', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('⚠️ بيانات الدخول غير صحيحة، يرجى المحاولة مرة أخرى.', 'danger')
            
    return render_template('login.html')

@admin_bp.route('/logout')
def admin_logout():
    """منطق الخروج وتأمين الجلسة"""
    logout_user()
    flash('تم تسجيل الخروج بنجاح.', 'info')
    return redirect(url_for('admin.admin_login'))
