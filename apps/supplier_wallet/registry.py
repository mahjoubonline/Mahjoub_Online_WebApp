# coding: utf-8
# 📂 apps/suppliers_orders/registry.py

from apps.suppliers_orders.routes import suppliers_orders_bp

def register_module(app):
    """
    تسجيل موديول الطلبات للموردين فقط دون إضافته للهيكل الديناميكي للإدارة.
    """
    app.register_blueprint(suppliers_orders_bp, url_prefix='/suppliers_orders')
    print("✅ [Registry] تم تسجيل موديول 'طلبات المورد' بنجاح.")
