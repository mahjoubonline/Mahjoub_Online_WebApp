from flask import Blueprint

admin_bp = Blueprint('admin_portal', __name__)

@admin_bp.route('/admin/dashboard')
def admin_dashboard():
    return "<h1 style='color:#D4AF37; background:#0A0A0A; text-align:center; padding:50px;'>🛡️ لوحة التحكم السيادية - إدارة الموردين</h1>"
