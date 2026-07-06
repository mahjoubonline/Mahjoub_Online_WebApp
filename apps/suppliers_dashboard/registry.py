# coding: utf-8
from apps.suppliers_dashboard.routes import suppliers_dashboard_bp

# البيانات المطلوبة لنظام التسجيل التلقائي في __init__.py
MODULE_NAME = "لوحة تحكم المورد"
MODULE_ICON = "fas fa-store"
SHOW_IN_SUPPLIER = True  # ليتم إضافته إلى SUPPLIER_MODULES
LINKS = {
    'الرئيسية': 'suppliers_dashboard.dashboard',
    'الإعدادات': 'suppliers_dashboard.settings',
    'سحب الأرباح': 'suppliers_dashboard.withdraw'
}

def register_module(app):
    """
    الدالة التي يستدعيها ملف __init__.py تلقائياً لتسجيل الموديول،
    مع التحقق من عدم تكرار التسجيل لتجنب أخطاء Flask.
    """
    if 'suppliers_dashboard' not in app.blueprints:
        app.register_blueprint(suppliers_dashboard_bp, url_prefix='/supplier')
        print("✅ [Registry]: تم تسجيل موديول 'suppliers_dashboard' بنجاح.")
    else:
        print("⚠️ [Registry]: موديول 'suppliers_dashboard' مسجل مسبقاً، تم التخطي.")
