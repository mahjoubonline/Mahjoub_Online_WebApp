# 📂 apps/vendors/routes.py

from flask import Blueprint, render_template, request, session, redirect, url_for
from .vendor_auth_service import vendor_login_required

# تعريف الـ Blueprint للموردين
vendors_bp = Blueprint('vendors', __name__, template_folder='templates')

@vendors_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    """صفحة تسجيل الدخول للموردين"""
    return render_template('vendor/login.html')

@vendors_bp.route('/dashboard')
@vendor_login_required  # <-- هذا هو الحارس الذي يحمي اللوحة
def dashboard():
    """لوحة تحكم المورد (محمية)"""
    return render_template('vendor/dashboard.html', vendor_name=session.get('vendor_name'))

@vendors_bp.route('/logout')
def logout():
    """تسجيل الخروج"""
    session.clear()
    return redirect(url_for('vendors.login_page'))
