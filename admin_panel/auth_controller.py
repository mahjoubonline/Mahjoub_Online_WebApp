from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from core.models.user import User
from core import db

class AdminAuthController:
    @staticmethod
    def login_logic():
        if current_user.is_authenticated and current_user.role == 'admin':
            return redirect(url_for('admin_panel.admin_dashboard'))

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username, role='admin').first()
            
            if user and user.check_password(password):
                login_user(user)
                flash('مرحباً بك في برج الرقابة السيادية.', 'success')
                return redirect(url_for('admin_panel.admin_dashboard'))
            else:
                flash('بيانات الدخول غير صحيحة.', 'danger')

        # تأكد أن المسار يبدأ بـ اسم المجلد الفرعي
        return render_template('admin_panel/login.html')

    @staticmethod
    def dashboard_logic():
        if current_user.role != 'admin':
            return redirect(url_for('admin_panel.admin_login'))
        return render_template('admin_panel/dashboard.html')

    @staticmethod
    def suppliers_logic():
        if current_user.role != 'admin':
            return redirect(url_for('admin_panel.admin_login'))
        return render_template('admin_panel/admin_suppliers_management.html')

    @staticmethod
    def sync_logic():
        if current_user.role != 'admin':
            return redirect(url_for('admin_panel.admin_login'))
        return render_template('admin_panel/product_review.html')

    @staticmethod
    def wallets_logic():
        if current_user.role != 'admin':
            return redirect(url_for('admin_panel.admin_login'))
        return render_template('admin_panel/wallets.html')

    @staticmethod
    def logout_logic():
        logout_user()
        flash('تم إنهاء الجلسة السيادية بنجاح.', 'info')
        return redirect(url_for('admin_panel.admin_login'))
