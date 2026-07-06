# coding: utf-8
from apps.suppliers_auth_portal.routes import suppliers_bp

def register_module(app):
    # التسجيل هنا هو الذي يربط الـ Blueprint باسمه 'suppliers_auth'
    app.register_blueprint(suppliers_bp, url_prefix='/supplier')
