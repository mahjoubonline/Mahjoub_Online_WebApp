# 📂 apps/utils/orders_engine.py
import logging
from apps.utils.bridge_engine import execute_query

logger = logging.getLogger(__name__)

class OrdersEngine:
    def get_all_orders(self):
        """جلب الطلبات من قمرة مع كافة الحقول المحددة"""
        query = """
        query {
          findAllOrders(input: { limit: 20, page: 1 }) {
            data {
              _id
              customer { name }
              createdAt
              status
              financialStatus
              fulfillmentStatus
              paymentMethod
              totalPrice { amount currency }
              items { productId price quantity }
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

    def get_pending_orders(self):
        """جلب الطلبات المعلقة فقط وتصفيتها برمجياً"""
        all_orders = self.get_all_orders()
        # التصفية بناءً على القيمة 'pending'
        return [o for o in all_orders if o.get('status') == 'pending']

    def sync_orders_from_source(self):
        """مزامنة الطلبات"""
        try:
            orders = self.get_all_orders()
            logger.info(f"Successfully synced {len(orders)} orders.")
            return True
        except Exception as e:
            logger.error(f"Sync failed: {str(e)}")
            return False
