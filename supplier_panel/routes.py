from flask import Blueprint
from flask_login import login_required
from .auth_logic import SupplierAuthLogic # استيراد المنطق من الملف الجديد

supplier_bp = Blueprint('supplier_panel', __name__, template_folder='templates')

@supplier_bp.route('/login', methods=['GET', 'POST'])
def supplier_login():
    return SupplierAuthLogic.login_process()

@supplier_bp.route('/dashboard')
@login_required
def supplier_dashboard():
    return SupplierAuthLogic.dashboard_process()

@supplier_bp.route('/my-products')
@login_required
def my_products():
    return SupplierAuthLogic.products_list_process()

@supplier_bp.route('/logout')
@login_required
def supplier_logout():
    return SupplierAuthLogic.logout_process()
