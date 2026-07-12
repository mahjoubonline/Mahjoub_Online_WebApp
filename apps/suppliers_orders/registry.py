# 📂 apps/suppliers_orders/registry.py

MODULE_NAME = "طلبات الزبائن"
MODULE_ICON = "fas fa-shopping-cart"
SHOW_IN_SUPPLIER = True

# اجعل الـ Endpoint هو المفتاح (Key) ليتوافق مع فلتر الـ available_endpoints
LINKS = {
    'suppliers_orders.index': 'إدارة الطلبات'
}

def register_module(app):
    from apps.suppliers_orders.routes import suppliers_orders_bp
    app.register_blueprint(suppliers_orders_bp, url_prefix='/supplier/orders')
    print("✅ [Registry]: تم تسجيل موديول 'suppliers_orders' بنجاح.")
