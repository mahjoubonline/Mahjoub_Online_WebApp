# coding: utf-8
from apps.suppliers_dashboard.routes import dashboard_bp

def register_module(app):
    """تسجيل لوحة تحكم المورد"""
    try:
        app.register_blueprint(dashboard_bp, url_prefix='/suppliers_dashboard')
        print("✅ [Registry]: تم تسجيل لوحة تحكم المورد بنجاح.")
    except Exception as e:
        print(f"🚨 [Registry Error]: فشل تسجيل لوحة المورد: {e}")
