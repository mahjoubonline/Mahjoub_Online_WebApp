# 📂 apps/utils/orders_engine.py
import logging
from apps.utils.bridge_engine import execute_query

logger = logging.getLogger(__name__)

def get_pending_orders():
    """
    جلب الطلبات مباشرة من قمرة لفرز الحالات المعلقة حياً ومباشراً في الذاكرة.
    """
    query = """
    query GetOrders {
      orders {
        id
        totalPrice
        status
        createdAt
      }
    }
    """
    result = execute_query(query)
    
    if not result or 'data' not in result:
        return []
        
    orders = result.get('data', {}).get('orders', [])
    
    # تصفية الطلبات المعلقة حياً في الذاكرة لسرعة العرض الفورية
    return [o for o in orders if o.get('status') == 'pending']
