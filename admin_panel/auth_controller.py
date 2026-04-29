from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from core.models.user import User

class AdminAuthController:
    """
    متحكم إدارة النظام.
    يضمن وصول الإدارة فقط إلى الصلاحيات العليا.
    """
    
    def login_logic(self):
        # منع الوصول لصفحة الدخول إذا كان المدير مسجلاً دخوله بالفعل
        if current_user.is_authenticated and current_user.is_admin():
            return redirect(url_for('admin_panel.admin_dashboard'))

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter_by(username=username).first()

            # التحقق من البيانات والرتبة (Admin)
            if not user or not user.check_password(password):
                flash('بيانات الدخول غير صحيحة.', 'danger')
                return render_template('admin_panel/login.html')

            if not user.is_admin():
                flash('عذراً، لا تمتلك صلاحيات الوصول لهذه المنطقة.', 'danger')
                return render_template('admin_panel/login.html')

            login_user(user)
            return redirect(url_for('admin_panel.admin_dashboard'))

        return render_template('admin_panel/login.html')

    def dashboard_logic(self):
        """لوحة التحكم المركزية للمنصة"""
        return render_template('admin_panel/dashboard.html')

    def suppliers_logic(self):
        """إدارة شركاء النجاح (الموردين)"""
        return render_template('admin_panel/suppliers_management.html')

    def logout_logic(self):
        logout_user()
        flash('تم تسجيل الخروج من لوحة الإدارة.', 'info')
        return redirect(url_for('admin_panel.admin_login'))
