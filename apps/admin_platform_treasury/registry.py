# coding: utf-8
from .routes import treasury_bp

def register_module(app):
    app.register_blueprint(treasury_bp, url_prefix='/admin/treasury')
    print("✅ [Registry]: تم تسجيل موديول 'admin_platform_treasury' بنجاح.")
