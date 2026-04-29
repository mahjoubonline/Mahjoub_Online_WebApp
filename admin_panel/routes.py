from flask import Blueprint
from .auth_controller import AdminAuthController

# تعريف البلوبرينت مع تحديد مجلد القوالب
admin_bp = Blueprint(
    'admin_panel', 
    __name__, 
    template_folder='templates'
)

auth_controller = AdminAuthController()

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    return auth_controller.login_logic()

@admin_bp.route('/dashboard')
def admin_dashboard():
    return auth_controller.dashboard_logic()

@admin_bp.route('/suppliers-management')
def manage_suppliers():
    return auth_controller.suppliers_logic()

@admin_bp.route('/logout')
def logout():
    return auth_controller.logout_logic()
