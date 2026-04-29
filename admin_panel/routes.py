from flask import Blueprint, render_template
from flask_login import login_required
from .auth_controller import AdminAuthController

# تعريف البلوبرينت الخاص بلوحة الإدارة مع تحديد مجلد القوالب
admin_bp = Blueprint('admin_panel', __name__, template_folder='templates')

# إنشاء نسخة من المتحكم لضمان عمل المنطق البرمجي داخل الكلاس بشكل سليم
auth_controller = AdminAuthController()

# --- مسارات بوابة الدخول والمغادرة ---

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    """بوابة الدخول الخاصة بإدارة محجوب أونلاين"""
    return auth_controller.login_logic()

@admin_bp.route('/logout')
@login_required
def logout():
    """إنهاء الجلسة والعودة للرئيسية"""
    return auth_controller.logout_logic()

# --- مسارات لوحة التحكم والإدارة ---

@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    """الواجهة الرئيسية للإدارة - لوحة التحكم الذكية"""
    return auth_controller.dashboard_logic()

@admin_bp.route('/suppliers-management')
@login_required
def manage_suppliers():
    """إدارة الموردين وشركاء النجاح"""
    return auth_controller.suppliers_logic()

@admin_bp.route('/product-review')
@login_required
def sync_now():
    """مراجعة المنتجات والمزامنة مع الموردين"""
    return auth_controller.sync_logic()

@admin_bp.route('/wallets')
@login_required
def wallets():
    """إدارة المحافظ المالية والحوكمة الرقمية"""
    return auth_controller.wallets_logic()
