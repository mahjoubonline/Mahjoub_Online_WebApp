# coding: utf-8
from apps.suppliers_dashboard.routes import suppliers_dashboard_bp

def register_module(app):
    # التسجيل ببادئة /supplier ليكون الرابط الكامل: /supplier/dashboard
    app.register_blueprint(suppliers_dashboard_bp, url_prefix='/supplier')
