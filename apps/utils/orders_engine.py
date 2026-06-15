# 📂 apps/utils/orders_engine.py
from apps.utils.bridge_engine import QumraBridgeEngine
from apps.extensions import db
from apps.models.order_db import Order
import logging

logger = logging.getLogger(__name__)

class OrdersEngine:
    def __init__(self):
        # نقوم بإنشاء نسخة من المحرك الموحد داخلياً
        self.bridge = QumraBridgeEngine()

    def sync_orders_to_db(self):
        try:
            logger.info("بدء جلب الطلبات من قمرة...")
            # استخدام النسخة مباشرة
            orders = self.bridge.fetch_latest_orders()
            
            if not orders:
                logger.warning("لم يتم جلب أي طلبات.")
                return 0

            count = 0
            for item in orders:
                order_id = str(item.get('_id') or '')
                if not order_id: continue
                
                order = Order.query.filter_by(order_id_qumra=order_id).first() or Order(order_id_qumra=order_id)
                
                order.total = float(item.get('totalPrice', 0))
                status_obj = item.get('status')
                order.status = status_obj.get('name', 'pending') if isinstance(status_obj, dict) else 'pending'
                
                account_obj = item.get('account')
                order.customer_name = account_obj.get('name', 'غير معروف') if isinstance(account_obj, dict) else 'غير معروف'
                
                db.session.add(order)
                count += 1
            
            db.session.commit()
            return count
            
        except Exception as e:
            logger.error(f"خطأ في معالجة بيانات الطلبات: {str(e)}")
            db.session.rollback()
            raise e
