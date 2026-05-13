from flask import Blueprint, render_template

# تأكد أن الاسم هنا هو admin_dashboard كما سجلناه في __init__.py
admin_dashboard = Blueprint('admin_dashboard', __name__, template_folder='templates')

@admin_dashboard.route('/')
@admin_dashboard.route('/dashboard')
def dashboard():
    # هذا المسار سيفتح لوحة التحكم المركزية
    return render_template('admin/admin_base.html')

@admin_dashboard.route('/suppliers')
def list_suppliers():
    # هذا المسار لعرض جدول الموردين (السجل)
    return render_template('admin/list_suppliers.html')
