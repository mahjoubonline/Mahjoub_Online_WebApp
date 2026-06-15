# 📂 apps/utils/orders_engine.py
from apps.utils.bridge_engine import QumraBridgeEngine
from apps.extensions import db
from apps.models.order_db import Order

class OrdersEngine(QumraBridgeEngine):
    def sync_orders_to_db(self):
        # استخدام المحرك الموحد الذي يعمل بنجاح
        orders = self.fetch_latest_orders()
        
        count = 0
        for item in orders:
            order_id = str(item.get('id'))
            if not order_id: continue
            
            order = Order.query.filter_by(order_id_qumra=order_id).first() or Order(order_id_qumra=order_id)
            
            # تحديث البيانات
            order.total = float(item.get('total', 0))
            order.status = item.get('status', 'pending')
            order.customer_name = item.get('customer', 'غير معروف')
            
            db.session.add(order)
            count += 1
        
        db.session.commit()
        return count
