# 📂 apps/suppliers_orders/registry.py
from apps.suppliers_orders.routes import suppliers_orders_bp

MODULE_NAME = "طلبات الموردين"
MODULE_ICON = "fa-shopping-cart"
LINKS = {"قائمة الطلبات": "supplier_orders_module_unique.dashboard"}

def register_module(app):
    # نستخدم app.blueprints للتحقق قبل التسجيل لتجنب الخطأ
    if 'supplier_orders_module_unique' not in app.blueprints:
        app.register_blueprint(suppliers_orders_bp, url_prefix='/suppliers_orders')
        print("✅ [Registry]: تم تسجيل موديول 'طلبات الموردين' (إدارة) بنجاح.")
