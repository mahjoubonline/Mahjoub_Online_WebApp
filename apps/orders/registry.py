# 📂 apps/orders/registry.py
from apps.orders.routes import orders_bp

def register_module(app):
    app.register_blueprint(orders_bp, url_prefix='/orders')
