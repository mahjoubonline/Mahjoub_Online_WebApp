# 📂 apps/suppliers_auth_portal/registry.py
from .routes import vendors_bp

def register_suppliers_auth(app):
    """تسجيل تلقائي لبوابة الموردين"""
    app.register_blueprint(vendors_bp, url_prefix='/suppliers_auth')
