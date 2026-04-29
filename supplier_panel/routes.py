from flask import Blueprint
from flask_login import login_required
from .auth_logic import SupplierAuthLogic

# تعريف البلوبرينت الخاص بالموردين
supplier_bp = Blueprint('supplier_panel', __name__, template_folder='templates')

@supplier_bp.route('/login', methods=['GET', 'POST'])
def supplier_login():
    # استدعاء منطق تسجيل الدخول
    return SupplierAuthLogic.login_process()

@supplier_bp.route('/dashboard')
@login_required
def supplier_dashboard():
    # استدعاء منطق لوحة التحكم
    return SupplierAuthLogic.dashboard_process()

@supplier_bp.route('/my-products')
@login_required
def my_products():
    # استدعاء منطق إدارة المنتجات
    return SupplierAuthLogic.products_list_process()

@supplier_bp.route('/logout')
@login_required
def supplier_logout():
    # استدعاء منطق تسجيل الخروج
    return SupplierAuthLogic.logout_process()
