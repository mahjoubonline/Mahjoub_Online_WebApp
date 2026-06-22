# 📂 apps/suppliers_auth_portal/registry.py
from .routes import suppliers_bp

def register_app(app):
    app.register_blueprint(suppliers_bp, url_prefix='/suppliers')
    print("✅ [System] تم تسجيل بوابة الموردين (Suppliers Portal) تلقائياً عبر Registry")
