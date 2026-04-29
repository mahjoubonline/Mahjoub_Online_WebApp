from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from core.models.user import User
from core import db

class SupplierAuthLogic:
    @staticmethod
    def login_process():
        # إذا كان المورد مسجلاً دخوله بالفعل، يتم توجيهه للوحة تحكمه
        if current_user.is_authenticated and current_user.role == 'supplier':
            return redirect(url_for('supplier_panel.supplier_dashboard'))

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            # البحث عن المورد والتأكد من دوره في النظام
            user = User.query.filter_by(username=username, role='supplier').first()
            
            if user and user.check_password(password):
                # التأكد من أن الحساب "معمد" (Approved) من قبل الإدارة
                if user.status == 'approved':
                    login_user(user)
                    flash('مرحباً بك في منصة التوريد الخاصة بك.', 'success')
                    return redirect(url_for('supplier_panel.supplier_dashboard'))
                else:
                    flash('حسابك لا يزال قيد المراجعة السيادية من قبل الإدارة.', 'warning')
            else:
                flash('بيانات الدخول غير صحيحة.', 'danger')

        # سيبحث Flask في supplier_panel/templates/supplier_panel/login.html
        return render_template('supplier_panel/login.html')

    @staticmethod
    def dashboard_process():
        if current_user.role != 'supplier':
            return redirect(url_for('supplier_panel.supplier_login'))
        return render_template('supplier_panel/dashboard.html')

    @staticmethod
    def products_list_process():
        if current_user.role != 'supplier':
            return redirect(url_for('supplier_panel.supplier_login'))
        return render_template('supplier_panel/my_products.html')

    @staticmethod
    def logout_process():
        logout_user()
        flash('تم تسجيل الخروج من بوابة الموردين بنجاح.', 'info')
        return redirect(url_for('supplier_panel.supplier_login'))
