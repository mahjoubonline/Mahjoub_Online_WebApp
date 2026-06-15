# 📂 apps/utils/orders_engine.py
from .bridge_engine import QumraBridgeEngine
from apps.extensions import db
from apps.models.order_db import Order

class OrdersEngine:
    def __init__(self):
        self.bridge = QumraBridgeEngine()

    def sync(self):
        query = """
        query { orders(first: 20) { data { _id totalPrice status { name } account { name } createdAt } } }
        """
        result = self.bridge.execute(query)
        orders = result.get("data", {}).get("orders", {}).get("data", [])
        
        for item in orders:
            order_id = str(item.get('_id'))
            order = Order.query.filter_by(order_id_qumra=order_id).first() or Order(order_id_qumra=order_id)
            order.total = float(item.get('totalPrice', 0))
            order.status = item.get('status', {}).get('name', 'pending')
            db.session.add(order)
        db.session.commit()
        return len(orders)
