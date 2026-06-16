# 📂 apps/utils/orders_engine.py

# الاستيرادات الآمنة في الأعلى
from apps.utils.bridge_engine import execute_query

def get_pending_orders():
    """
    جلب الطلبات مباشرة من قمرة لفرز الحالات المعلقة.
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
    
    # تصفية الطلبات المعلقة محلياً لسرعة العرض
    return [o for o in orders if o.get('status') == 'pending']
