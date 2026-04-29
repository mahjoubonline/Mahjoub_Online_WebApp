from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
# استيراد موديل المستخدم من النواة
from core.models.user import User

# تعريف البلوبرينت مع تحديد مجلد القوالب الأساسي
admin_bp = Blueprint(
    'admin_panel', 
    __name__, 
    template_folder='templates'
)

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    """منطق تسجيل دخول الإدارة الموحد"""
    
    # 1. إذا كان المسؤول مسجلاً دخوله بالفعل، يتم توجيهه للوحة التحكم
    if current_user.is_authenticated and current_user.is_admin():
        return redirect(url_for('admin_panel.admin_dashboard'))

    if request.method == 'POST':
        # استخدام username بناءً على إعدادات الموديل في النواة
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        # البحث عن المستخدم في قاعدة البيانات
        user = User.query.filter_by(username=username).first()

        # 2. التحقق من صحة البيانات والصلاحية (Admin Role)
        if user and user.check_password(password) and user.is_admin():
            login_user(user, remember=remember)
            return redirect(url_for('admin_panel.admin_dashboard'))
        
        # رسالة تنبيه في حال فشل الدخول
        flash('بيانات الدخول غير صحيحة أو لا تملك صلاحية الوصول للإدارة.', 'danger')

    # استدعاء القالب من المسار الفرعي الذي حددته
    return render_template('admin_panel/login.html')

@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    """لوحة التحكم المركزية للإدارة"""
    
    # حماية إضافية لضمان أن الموردين لا يمكنهم الدخول هنا
    if not current_user.is_admin():
        flash('هذه اللوحة مخصصة لمدير النظام فقط.', 'warning')
        return redirect(url_for('admin_panel.admin_login'))
    
    return render_template('admin_panel/dashboard.html')

@admin_bp.route('/logout')
@login_required
def logout():
    """تسجيل خروج المسؤول بأمان"""
    logout_user()
    flash('تم تسجيل الخروج بنجاح من لوحة الإدارة.', 'info')
    return redirect(url_for('admin_panel.admin_login'))
