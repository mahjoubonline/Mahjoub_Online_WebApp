from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from core.models.user import User  # تأكد من مسار موديل المستخدم لديك
from core import db

class SupplierController:
    def __init__(self):
        pass

    def login_logic(self):
        """منطق تسجيل دخول الموردين"""
        if current_user.is_authenticated:
            return redirect(url_for('supplier_panel.supplier_dashboard'))
        
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email, role='supplier').first()
            
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('supplier_panel.supplier_dashboard'))
            else:
                flash('بيانات الدخول غير صحيحة أو لست مورداً مسجلاً', 'danger')
        
        return render_template('supplier/login.html')

    def dashboard_logic(self):
        """عرض إحصائيات المورد"""
        return render_template('supplier/dashboard.html')

    def products_logic(self):
        """إدارة منتجات المورد"""
        return render_template('supplier/products.html')

    def orders_logic(self):
        """إدارة الطلبات الواردة"""
        return render_template('supplier/orders.html')

    def settings_logic(self):
        """إعدادات الحساب والربط التقني"""
        return render_template('supplier/settings.html')

    def logout_logic(self):
        """تسجيل الخروج"""
        logout_user()
        return redirect(url_for('supplier_panel.supplier_login'))
