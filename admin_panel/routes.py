from flask import Blueprint
from flask_login import login_required
from .auth_controller import AdminAuthController # استيراد المنطق

admin_bp = Blueprint('admin_panel', __name__, template_folder='templates')

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    return AdminAuthController.login_logic()

@admin_bp.route('/logout')
@login_required
def logout():
    return AdminAuthController.logout_logic()

@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    return AdminAuthController.dashboard_logic()

@admin_bp.route('/suppliers-management')
@login_required
def manage_suppliers():
    return AdminAuthController.suppliers_logic()

@admin_bp.route('/product-review')
@login_required
def sync_now():
    return AdminAuthController.sync_logic()

@admin_bp.route('/wallets')
@login_required
def wallets():
    return AdminAuthController.wallets_logic()

# تأكد من وجود template_folder='templates'
admin_bp = Blueprint('admin_panel', __name__, template_folder='templates')

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    return AdminAuthController.login_logic()
