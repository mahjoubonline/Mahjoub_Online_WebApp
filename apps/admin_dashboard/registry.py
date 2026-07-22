# coding: utf-8
# 📂 apps/admin_dashboard/registry.py

"""
تسجيل تطبيق لوحة تحكم الإدارة في المنصة
"""

# ✅ بيانات الموديول
MODULE_NAME = "لوحة التحكم"
MODULE_ICON = "fas fa-chart-line"
SHOW_IN_SUPPLIER = False

# ✅ الروابط التي تظهر في القائمة الجانبية للإدارة
LINKS = {
    'admin_dashboard_bp.dashboard': '📊 لوحة التحكم'
}


def register_module(app):
    """
    تسجيل موديول لوحة تحكم الإدارة في التطبيق الرئيسي
    """
    from apps.admin_dashboard.routes import admin_dashboard_bp
    
    if 'admin_dashboard_bp' not in app.blueprints:
        app.register_blueprint(admin_dashboard_bp, url_prefix='/admin')
        print("✅ [Registry]: تم تسجيل 'admin_dashboard_bp' بنجاح.")
    
    return app
