from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from core.models.user import User 
from . import admin_bp

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    """بوابة الولوج السيادية - التحقق من هوية القادة والموردين"""
    
    # إذا كان المستخدم مسجلاً دخوله بالفعل، نوجهه مباشرة حسب دوره
    if current_user.is_authenticated:
        return redirect_by_role(current_user)
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # البحث عن المستخدم في الترسانة الرقمية
        user = User.query.filter_by(username=username).first()
        
        # التحقق من مطابقة مفتاح التشفير وصلاحية الحساب
        if user and user.check_password(password):
            if not user.is_active_account:
                flash('هذا الحساب معلق حالياً من قبل الإدارة المركزية.', 'warning')
                return redirect(url_for('admin.admin_login'))
            
            # تسجيل الدخول وتوجيه المستخدم
            login_user(user)
            return redirect_by_role(user)
        else:
            flash('فشل التوثيق.. تأكد من المعرف ومفتاح التشفير.', 'danger')
            
    return render_template('login.html')

def redirect_by_role(user):
    """نظام التوجيه الذكي بناءً على مصفوفة الأدوار"""
    
    if user.role == 'admin':
        # توجيه القائد علي محجوب إلى برج الرقابة
        return redirect(url_for('admin.admin_dashboard'))
    
    elif user.role == 'supplier':
        # توجيه شركاء الترسانة (الموردين) إلى لوحة التحكم الخاصة بهم
        # ملاحظة: تأكد من تسجيل بلوبرنت 'supplier' في core/__init__.py لاحقاً
        return redirect(url_for('supplier.dashboard'))
    
    else:
        # توجيه العملاء والمتسوقين إلى واجهة المتجر الرئيسية
        return redirect(url_for('main.index'))

@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    """برج الرقابة المركزية - حصري للقائد فقط"""
    
    # حماية إضافية لضمان عدم دخول أي دور آخر غير 'admin'
    if current_user.role != 'admin':
        flash('تحذير: محاولة وصول غير مصرح بها لبرج الرقابة.', 'danger')
        return redirect(url_for('admin.admin_login'))
        
    return render_template('dashboard.html')

@admin_bp.route('/logout')
@login_required
def logout():
    """إنهاء الجلسة السيادية والعودة لبوابة الدخول"""
    logout_user()
    flash('تم إنهاء الجلسة بنجاح. نراك لاحقاً في منصة محجوب.', 'success')
    return redirect(url_for('admin.admin_login'))
