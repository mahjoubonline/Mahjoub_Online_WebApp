# 📂 apps/vendors/registry.py
from apps.vendors.routes import vendors_bp

def register_app(app):
    """
    هذه الدالة تستدعى تلقائياً من قبل المصنع الرئيسي (apps/__init__.py).
    تقوم بتسجيل مسارات الموردين (Blueprints) تحت بادئة المسار '/vendors'.
    """
    app.register_blueprint(vendors_bp, url_prefix='/vendors')
    print("✅ [Registry] تم تسجيل وحدة الموردين بنجاح على المسار /vendors")
