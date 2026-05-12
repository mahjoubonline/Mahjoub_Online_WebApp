
from flask import Blueprint, render_template

# نحدد هنا اسم المجلد templates لكي يعرف Flask أين يبحث
admin_bp = Blueprint('admin', __name__, template_folder='templates')

@admin_bp.route('/dashboard')
def dashboard():
    # استدعاء الملف من داخل مجلد admin الفرعي
    return render_template('admin/dashboard_content.html')

@admin_bp.route('/suppliers/manage')
def manage_suppliers():
    return render_template('admin/dashboard_content.html', title="الموردون المعتمدون")
