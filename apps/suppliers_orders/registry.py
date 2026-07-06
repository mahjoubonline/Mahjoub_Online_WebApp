# coding: utf-8
# 📂 apps/suppliers_orders/registry.py

from apps.suppliers_orders.routes import suppliers_orders_bp

# متغيرات يتوقعها نظام Auto-Discovery في __init__.py
MODULE_NAME = "طلبات الزبائن"
MODULE_ICON = "fas fa-shopping-cart"
LINKS = {
    "إدارة الطلبات": "suppliers_orders_portal.dashboard"
}

def register_module(app):
    try:
        app.register_blueprint(suppliers_orders_bp, url_prefix='/suppliers/orders')
        print("✅ [Registry]: تم تسجيل موديول 'suppliers_orders' بنجاح.")
    except Exception as e:
        print(f"🚨 [Registry Error]: {e}")
