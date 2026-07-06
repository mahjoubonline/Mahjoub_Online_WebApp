# 📂 apps/suppliers_orders/registry.py
from apps.suppliers_orders.routes import suppliers_orders_bp

MODULE_NAME = "طلبات الموردين"
MODULE_ICON = "fa-truck"
LINKS = {"لوحة التحكم": "supplier_orders_module_unique.dashboard"}

def register_module(app):
    # نستخدم url_prefix هنا وليس في ملف routes.py
    app.register_blueprint(suppliers_orders_bp, url_prefix='/suppliers')
