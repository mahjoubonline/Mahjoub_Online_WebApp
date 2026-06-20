# 📂 apps/vendors/registry.py
from apps.vendors.routes import vendors_bp

def register_vendors_module(app):
    """
    هذه الدالة تُستدعى تلقائياً من قبل محرك التطبيق الديناميكي
    لربط مسارات الموردين بالتطبيق الأساسي.
    """
    app.register_blueprint(vendors_bp, url_prefix='/vendors')
