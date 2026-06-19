from flask import render_template
# استيراد الـ Blueprint الذي عرفناه سابقاً في __init__.py الخاص بالموردين
from . import vendors_bp 

@vendors_bp.route('/dashboard')
def dashboard():
    # هنا تضع كود عرض لوحة التحكم الخاصة بالمورد
    # ملاحظة: الملف يجب أن يكون في: apps/vendors/templates/vendor/dashboard.html
    return render_template('vendor/dashboard.html')

@vendors_bp.route('/profile')
def profile():
    return "هذه صفحة المورد الشخصية"
