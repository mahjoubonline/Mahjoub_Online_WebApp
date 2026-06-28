# coding: utf-8
# 📂 apps/orders/registry.py

from apps.orders.routes import orders_bp

def register_module(app):
    """
    هذه الدالة هي التي يبحث عنها ملف apps/__init__.py 
    للقيام بالتسجيل التلقائي لموديول الطلبات.
    """
    app.register_blueprint(orders_bp, url_prefix='/orders')
    print("✅ [Registry]: تم تسجيل موديول 'Orders' بنجاح.")
