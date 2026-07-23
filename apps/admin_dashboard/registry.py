# coding: utf-8
# 📂 apps/admin_dashboard/registry.py

"""
تسجيل تطبيق لوحة تحكم الإدارة في المنصة
"""

MODULE_NAME = "لوحة تحكم الإدارة"
MODULE_ICON = "fas fa-chart-line"
SHOW_IN_SUPPLIER = False  # ❌ لا يظهر للموردين

LINKS = {
    'admin_dashboard_bp.dashboard': '📊 لوحة التحكم'
}


def register_module(app):
    """تسجيل Blueprint لوحة تحكم الإدارة"""
    try:
        from apps.admin_dashboard.routes import admin_dashboard_bp
        
        if 'admin_dashboard_bp' not in app.blueprints:
            app.register_blueprint(admin_dashboard_bp, url_prefix='/admin')
            print("✅ [Registry]: تم تسجيل 'admin_dashboard_bp' بنجاح.")
    except Exception as e:
        print(f"❌ [Registry]: خطأ في تسجيل admin_dashboard: {e}")
    
    return app
