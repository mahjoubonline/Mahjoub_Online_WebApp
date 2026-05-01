from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from core.models.user import User 
from . import admin_bp

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    # إذا كان المستخدم مسجلاً دخوله بالفعل، يتم توجيهه حسب رتبته السيادية
    if current_user.is_authenticated:
        return redirect_by_role(current_user)
    
    if request.method == 'POST':
        # جلب البيانات مع تنظيف المسافات الزائدة (strip) لضمان الدقة
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # 1. البحث عن المستخدم في قاعدة البيانات (الترسانة الرقمية)
        user = User.query.filter_by(username=username).first()
        
        # المرحلة الأولى: فحص وجود الهوية
        if not user:
            flash(f'⚠️ تنبيه: اسم المستخدم "{username}" غير موجود في قاعدة البيانات.', 'danger')
            return redirect(url_for('admin.admin_login'))
        
        # المرحلة الثانية: فحص مطابقة مفتاح التشفير (الهاش)
        if not user.check_password(password):
            flash('❌ كلمة المرور غير صحيحة. يرجى التأكد من مفتاح التشفير الخاص بك.', 'danger')
            return redirect(url_for('admin.admin_login'))
        
        # المرحلة الثالثة: التأكد من حالة الحساب (نشط أم معلق)
        if not user.is_active_account:
            flash('🚫 هذا الحساب موجود ولكنه معلق حالياً من قبل الإدارة المركزية.', 'warning')
            return redirect(url_for('admin.admin_login'))
        
        # تنفيذ عملية الولوج وتثبيت الجلسة
        login_user(user)
        flash(f'أهلاً بك يا {user.username}. تم الدخول بنجاح إلى برج الرقابة.', 'success')
        return redirect_by_role(user)
            
    return render_template('login.html')

def redirect_by_role(user):
    """توجيه القائد أو المورد إلى الواجهة المخصصة له"""
    if user.role == 'admin':
        return redirect(url_for('admin.admin_dashboard'))
    elif user.role == 'supplier':
        return redirect(url_for('supplier.dashboard'))
    
    # التوجيه الافتراضي
    return redirect(url_for('main.index'))

@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    """لوحة تحكم القائد - برج الرقابة المركزية"""
    if current_user.role != 'admin':
        flash('عذراً، لا تملك صلاحيات الولوج إلى المناطق السيادية.', 'danger')
        return redirect(url_for('admin.admin_login'))
    
    return render_template('dashboard.html')

@admin_bp.route('/logout')
@login_required
def logout():
    """إنهاء الجلسة والولوج الآمن للخروج"""
    logout_user()
    flash('تم تسجيل الخروج بنجاح من نظام محجوب أونلاين.', 'success')
    return redirect(url_for('admin.admin_login'))
