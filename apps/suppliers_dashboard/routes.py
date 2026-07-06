# coding: utf-8
# 📂 apps/suppliers_auth/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
# تأكد من استيراد نموذج المورد الخاص بك هنا
from apps.models.supplier_db import Supplier 

suppliers_auth_bp = Blueprint('suppliers_auth', __name__, template_folder='templates')

@suppliers_auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # ... كود التحقق من البيانات هنا ...
        # عند نجاح الدخول:
        login_user(user)
        # هذا هو السطر الأهم:
        return redirect(url_for('suppliers_dashboard.dashboard'))
    return render_template('suppliers/login.html')

@suppliers_auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('suppliers_auth.login'))
