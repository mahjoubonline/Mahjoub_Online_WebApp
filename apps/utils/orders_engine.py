# 📂 apps/utils/orders_engine.py
import logging
from apps.utils.bridge_engine import execute_query

logger = logging.getLogger(__name__)

def get_pending_orders():
    """جلب الطلبات المعلقة مباشرة من API قمرة"""
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
        
        # استخراج البيانات وتصفية المعلق فقط
        orders = result.get('data', {}).get('findAllOrders', {}).get('data', [])
        return [o for o in orders if o.get('status') == 'pending']
    except Exception as e:
        logger.error(f"Error fetching direct from Qumra: {str(e)}")
        return []
