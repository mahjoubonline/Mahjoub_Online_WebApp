# coding: utf-8
from apps.suppliers_dashboard.routes import suppliers_dashboard_bp

MODULE_NAME = "لوحة تحكم المورد"
MODULE_ICON = "fas fa-store"
SHOW_IN_SUPPLIER = True
LINKS = {
    'الرئيسية': 'suppliers_dashboard.dashboard',
    'الإعدادات': 'suppliers_dashboard.settings'
}

def register_module(app):
    """
    تسجيل الموديول مع التحقق من عدم تكرار التسجيل لتجنب الخطأ.
    """
    # التحقق من أن الـ Blueprint غير مسجل مسبقاً في التطبيق
    if 'suppliers_dashboard' not in app.blueprints:
        app.register_blueprint(suppliers_dashboard_bp, url_prefix='/supplier')
        print("✅ [Registry]: تم تسجيل موديول 'suppliers_dashboard' بنجاح.")
    else:
        print("⚠️ [Registry]: موديول 'suppliers_dashboard' مسجل مسبقاً، تم التخطي.")
