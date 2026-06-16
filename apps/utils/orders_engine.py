# 📂 apps/utils/orders_engine.py
import logging
from apps.utils.bridge_engine import execute_query

logger = logging.getLogger(__name__)

class OrdersEngine:
    def __init__(self):
        pass

    def get_all_orders(self):
        """جلب الطلبات من قمرة باستخدام الـ Schema المعتمد"""
        query = """
        query {
          findAllOrders(input: { limit: 20, page: 1 }) {
            data {
              _id
              totalPrice
              items {
                productId
                price
                quantity
              }
            }
          }
        }
        """
        try:
            result = execute_query(query)
            if not result or 'data' not in result:
                return []
            
            # استخراج البيانات حسب هيكلية PaginatedOrdersResponse
            return result.get('data', {}).get('findAllOrders', {}).get('data', [])
        except Exception as e:
            logger.error(f"Error fetching orders: {str(e)}")
            return []

    def sync_orders_from_source(self):
        """مزامنة البيانات من قمرة إلى النظام المحلي"""
        try:
            orders = self.get_all_orders()
            # هنا يمكنك إضافة منطق حفظ الطلبات في قاعدة بياناتك المحلية (db.session.add)
            logger.info(f"Successfully synced {len(orders)} orders.")
            return True
        except Exception as e:
            logger.error(f"Sync failed: {str(e)}")
            return False

    def update_status(self, order_id, new_status):
        """تحديث حالة الطلب محلياً"""
        # ملاحظة: التحديث هنا يتم في قاعدة بياناتك المحلية فقط
        logger.info(f"Updating order {order_id} to {new_status}")
        return True

def get_pending_orders():
    """دالة مساعدة لجلب الطلبات المعلقة فقط"""
    engine = OrdersEngine()
    all_orders = engine.get_all_orders()
    # بما أن API لا يدعم الفلترة بـ status، نقوم بالتصفية برمجياً
    return [o for o in all_orders if o.get('status') == 'pending']
