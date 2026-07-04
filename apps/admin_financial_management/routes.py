# coding: utf-8
# 📂 apps/admin_financial_management/routes.py

from flask import Blueprint, render_template
from flask_login import login_required

# تعريف الـ Blueprint
# تم ضبط اسم الـ Blueprint ليكون 'financial_bp' ليتطابق مع ما هو معرف في registry.py
financial_bp = Blueprint(
    'financial_bp', 
    __name__, 
    template_folder='templates'
)

@financial_bp.route('/wallets', methods=['GET'])
@login_required
def manage_wallets():
    """
    صفحة إدارة المحافظ المالية.
    هذا المسار سيتم تسجيله تلقائياً تحت url_prefix='/admin/financial'
    ليصبح المسار النهائي: /admin/financial/wallets
    """
    # تأكد أن ملف القالب موجود في المسار التالي:
    # apps/admin_financial_management/templates/admin_financial_management/admin_financial_management.html
    return render_template('admin_financial_management/admin_financial_management.html')
