# 📂 apps/utils/sync_all.py
from .orders_engine import OrdersEngine
from .products_engine import ProductsEngine

def sync_everything():
    orders_count = OrdersEngine().sync_orders_to_db()
    products_count = ProductsEngine().sync_products_to_db()
    return {"orders": orders_count, "products": products_count}
