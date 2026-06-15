# 📂 apps/utils/orders_engine.py
import hashlib
from apps.utils.bridge_engine import QumraBridgeEngine
from apps.extensions import db
from apps.models.order_db import Order
import logging

logger = logging.getLogger(__name__)

class OrdersEngine:
    def __init__(self):
        self.bridge = QumraBridgeEngine()

    def sync_orders_to_db(self):
        try:
            orders = self.bridge.fetch_latest_orders()
            if not orders: return 0
            
            count = 0
            for item in orders:
                # توليد بصمة فريدة للطلب إذا لم يوجد _id
                data_str = f"{item.get('totalPrice')}-{item.get('createdAt')}-{item.get('account', {}).get('name')}"
                fingerprint = hashlib.md5(data_str.encode()).hexdigest()
                qumra_id = str(item.get('_id') or fingerprint)
                
                # البحث عن الطلب أو إنشاؤه
                order = Order.query.filter_by(order_id_qumra=qumra_id).first()
                if not order:
                    order = Order(order_id_qumra=qumra_id)
                    db.session.add(order)
                
                # تحديث البيانات (تلقائي)
                order.total = float(item.get('totalPrice', 0))
                order.status = item.get('status', {}).get('name', 'pending')
                order.customer_name = item.get('account', {}).get('name', 'غير معروف')
                order.raw_data = item
                
                count += 1
            
            db.session.commit()
            return count
        except Exception as e:
            logger.error(f"Sync Error: {str(e)}")
            db.session.rollback()
            raise e
