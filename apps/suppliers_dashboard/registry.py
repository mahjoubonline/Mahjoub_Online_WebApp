# 📂 apps/suppliers_dashboard/registry.py
from apps.suppliers_dashboard.routes import dashboard_bp

def register_app(app):
    """
    هذه الدالة تستدعى تلقائياً من قبل المصنع الرئيسي (apps/__init__.py).
    تقوم بتسجيل مسارات لوحة تحكم المورد (Blueprints) تحت بادئة المسار '/suppliers_dashboard'.
    """
    app.register_blueprint(dashboard_bp, url_prefix='/suppliers_dashboard')
    print("✅ [Registry] تم تسجيل وحدة لوحة تحكم المورد بنجاح على المسار /suppliers_dashboard")
