# 📂 apps/suppliers_dashboard/registry.py
def register_module(app):
    from apps.suppliers_dashboard.routes import suppliers_dashboard_bp # استيراد محلي
    if 'suppliers_dashboard' not in app.blueprints:
        app.register_blueprint(suppliers_dashboard_bp, url_prefix='/supplier')
