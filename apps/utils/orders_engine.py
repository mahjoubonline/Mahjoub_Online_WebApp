from .bridge_engine import QumraBridgeEngine
from apps.extensions import db
from apps.models.order_db import Order

class OrdersEngine(QumraBridgeEngine):
    def sync_orders_to_db(self):
        query = """
        query {
            orders(first: 20) {
                data {
                    _id totalPrice status { name } account { name } createdAt
                }
            }
        }
        """
        result = self.execute_query(query)
        data = result.get("data", {}).get("orders", {}).get("data", [])
        count = 0
        for item in data:
            order_id = str(item.get('_id'))
            order = Order.query.filter_by(order_id_qumra=order_id).first() or Order(order_id_qumra=order_id)
            order.total = float(item.get('totalPrice', 0))
            order.status = item.get('status', {}).get('name', 'pending')
            order.customer_name = item.get('account', {}).get('name', 'غير معروف')
            db.session.add(order)
            count += 1
        db.session.commit()
        return count
