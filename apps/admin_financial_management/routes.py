# coding: utf-8
# 📂 apps/admin_financial_management/routes.py

from flask import Blueprint, render_template
from flask_login import login_required

# تعريف الـ Blueprint
# تأكد أن اسم الـ Blueprint هنا هو نفس الاسم المستخدم في registry.py
financial_bp = Blueprint(
    'financial_bp', 
    __name__, 
    template_folder='templates'
)

@financial_bp.route('/wallets', methods=['GET'])
@login_required
def manage_wallets():
    """
    صفحة إدارة المحافظ المالية
    تم تغيير اسم الدالة لتطابق الرابط في registry.py
    """
    # هنا ستضع الكود الخاص بجلب البيانات لاحقاً
    # تأكد من وجود الملف في المسار: apps/admin_financial_management/templates/admin_financial_management/admin_financial_management.html
    return render_template('admin_financial_management/admin_financial_management.html')
