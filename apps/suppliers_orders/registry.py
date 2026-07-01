# coding: utf-8
# 📂 apps/suppliers_orders/registry.py

from apps.suppliers_orders.routes import suppliers_orders_bp

def register_module(app):
    """
    هذه الدالة هي التي يبحث عنها ملف apps/__init__.py 
    للقيام بالتسجيل التلقائي لموديول طلبات الموردين.
    """
    app.register_blueprint(suppliers_orders_bp, url_prefix='/suppliers-orders')
    print("✅ [Registry]: تم تسجيل موديول 'Suppliers Orders' بنجاح.")
