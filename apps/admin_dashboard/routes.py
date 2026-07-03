# coding: utf-8
# 📂 apps/admin_dashboard/routes.py

from flask import Blueprint, render_template, current_app
from flask_login import login_required

# 1. إنشاء الـ Blueprint
# الاسم 'admin_dashboard' هو المرجع الأساسي في url_for
admin_dashboard = Blueprint(
    'admin_dashboard', 
    __name__, 
    template_folder='templates'
)

# 2. تعريف المسار (Route)
@admin_dashboard.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """
    عرض لوحة تحكم النظام الرئيسية مع التحقق الديناميكي من الموديولات.
    تنبيه: مسار الملف المتوقع هو apps/admin_dashboard/templates/admin/dashboard.html
    """
    
    # التحقق الديناميكي من وجود الموديولات في الـ app لتجنب أي أخطاء في العرض
    # نستخدم current_app.blueprints للتحقق من الموديولات المسجلة برمجياً
    registered_modules = {
        'admin_suppliers_list': 'suppliers_bp' in current_app.blueprints,
        'finance_module': 'treasury_bp' in current_app.blueprints
    }
    
    # تهيئة البيانات الأساسية (سيتم استبدال القيم ببيانات من قاعدة البيانات لاحقاً)
    context = {
        "total_suppliers": 0,
        "total_balance_sar": 0.00,
        "total_balance_yer": 0.00,
        "total_balance_usd": 0.00,
        "recent_transactions": [],
        "registered_modules": registered_modules
    }
    
    # Render template يتطلب وجود ملف dashboard.html داخل مجلد templates/admin/
    return render_template('admin/dashboard.html', **context)
