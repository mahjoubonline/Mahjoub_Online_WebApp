from flask import Blueprint, render_template

# تأكد من أن الاسم هنا مطابق لما نستورده في run.py
admin_dashboard = Blueprint('admin_dashboard', __name__, template_folder='templates')

@admin_dashboard.route('/')
@admin_dashboard.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard_content.html')
