from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from core.models.user import User
from core.models.supplier import Supplier
from core import db

# تعريف البلوبرنت الخاص بالإدارة المركزية
admin_panel = Blueprint('admin_panel', __name__, template_folder='templates')

@admin_panel.route('/login', methods=['GET', 'POST'])
def admin_login():
    # منع المسؤول المسجل دخولاً بالفعل من رؤية صفحة الدخول
    if current_user.is_authenticated and getattr(current_user, 'role', None) == 'admin':
        return redirect(url_for('admin_panel.admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        # التحقق من الهوية والدور (يجب أن يكون admin)
        if user and user.check_password(password) and getattr(user, 'role', None) == 'admin':
            login_user(user)
            return redirect(url_for('admin_panel.admin_dashboard'))
        else:
            flash('فشل الوصول: بيانات الاعتماد غير صالحة لدخول الترسانة المركزية.', 'danger')
            
    return render_template('admin_panel/admin_login.html')

@admin_panel.route('/dashboard')
@login_required
def admin_dashboard():
    # حماية المسار السيادي: التأكد من أن المستخدم "أدمن"
    if getattr(current_user, 'role', None) != 'admin':
        flash('ليس لديك صلاحيات الوصول إلى القيادة المركزية.', 'danger')
        return redirect(url_for('main.index'))

    # جلب إحصائيات سريعة للوحة التحكم
    total_suppliers = Supplier.query.count()
    # يمكنك إضافة المزيد من الإحصائيات هنا (مثل عدد المنتجات، الطلبات، إلخ)
    
    return render_template(
        'admin_panel/dashboard.html',
        total_suppliers=total_suppliers
    )

@admin_panel.route('/suppliers/manage')
@login_required
def manage_suppliers():
    if getattr(current_user, 'role', None) != 'admin':
        return redirect(url_for('main.index'))
    
    suppliers = Supplier.query.all()
    return render_template('admin_panel/manage_suppliers.html', suppliers=suppliers)

@admin_panel.route('/logout')
@login_required
def logout():
    """
    هذا هو المسار الذي كان يسبب BuildError.
    تم تعريفه الآن باسم 'logout' داخل بلوبرنت 'admin_panel'.
    """
    logout_user()
    flash('تم إنهاء الجلسة السيادية وتأمين النظام.', 'success')
    return redirect(url_for('admin_panel.admin_login'))
