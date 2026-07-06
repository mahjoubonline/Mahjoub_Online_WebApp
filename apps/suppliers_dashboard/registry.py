# coding: utf-8
from apps.suppliers_dashboard.routes import suppliers_dashboard_bp # تأكد من تطابق الاسم

def register_module(app):
    app.register_blueprint(suppliers_dashboard_bp, url_prefix='/supplier')
