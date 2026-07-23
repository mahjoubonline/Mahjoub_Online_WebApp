# coding: utf-8
# 📂 apps/suppliers_dashboard/registry.py

"""
تسجيل تطبيق لوحة تحكم الموردين في المنصة
"""

# ✅ بيانات الموديول
MODULE_NAME = "لوحة التحكم"
MODULE_ICON = "fas fa-home"
SHOW_IN_SUPPLIER = True

# ✅ الروابط التي تظهر في القائمة الجانبية للمورد
LINKS = {
    'suppliers_dashboard.dashboard': '📊 لوحة التحكم'
}


def register_module(app):
    """
    تسجيل موديول لوحة التحكم (Dashboard) فقط
    """
    from apps.suppliers_dashboard.dashboard_routes import suppliers_dashboard_bp
    
    if 'suppliers_dashboard' not in app.blueprints:
        app.register_blueprint(suppliers_dashboard_bp, url_prefix='/supplier')
        print("✅ [Registry]: تم تسجيل 'suppliers_dashboard' بنجاح.")
    
    return app
