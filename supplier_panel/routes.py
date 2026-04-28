from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from core import db
from core.models.user import User
# استيراد دالة التحقق التي برمجناها سابقاً
from .auth_logic import handle_supplier_auth

# 1. تعريف البلوبرينت (Blueprint)
# تم استخدامه بدلاً من app مباشرة لتفادي Circular Import
supplier_bp = Blueprint('supplier_panel', __name__, template_folder='templates')

# 2. مسار تسجيل الدخول (Login)
@supplier_bp.route('/login', methods=['GET', 'POST'])
def supplier_login():
    # منع المستخدم المسجل بالفعل من العودة لصفحة الدخول
    if current_user.is_authenticated and current_user.role == 'supplier':
        return redirect(url_for('supplier_panel.supplier_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # استدعاء منطق التحقق السيادي
        user = handle_supplier_auth(username, password)
        
        if user:
            # النجاح: تسجيل الدخول والتوجه للوحة التحكم
            login_user(user)
            flash(f'مرحباً بك في نظام التوريد، {user.username}', 'success')
            return redirect(url_for('supplier_panel.supplier_dashboard'))
        
        # في حالة الفشل، تظهر الرسائل المبرمجة في auth_logic تلقائياً عبر flash

    return render_template('supplier_login.html')

# 3. لوحة تحكم المورد (Dashboard)
@supplier_bp.route('/dashboard')
@login_required
def supplier_dashboard():
    # فحص الرتبة لضمان أمن النظام
    if current_user.role != 'supplier':
        flash('وصول غير مصرح به لبرج الموردين.', 'danger')
        return redirect(url_for('admin_panel.admin_login'))
        
    return render_template('supplier_dashboard.html', user=current_user)

# 4. تسجيل الخروج (Logout)
@supplier_bp.route('/logout')
@login_required
def supplier_logout():
    logout_user()
    flash('تم إنهاء الجلسة اللامركزية بنجاح.', 'info')
    return redirect(url_for('supplier_panel.supplier_login'))
