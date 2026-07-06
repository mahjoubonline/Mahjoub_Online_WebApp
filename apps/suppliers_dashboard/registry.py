# coding: utf-8
# تأكد من أن الاستيراد صحيح تماماً وموجود في المسار
from apps.suppliers_dashboard.routes import suppliers_dashboard_bp

def register_module(app):
    if 'suppliers_dashboard' not in app.blueprints:
        app.register_blueprint(suppliers_dashboard_bp, url_prefix='/supplier')
        print("✅ [Registry]: تم تسجيل 'suppliers_dashboard' بنجاح.")
