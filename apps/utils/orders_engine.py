# 📂 apps/utils/orders_engine.py
from apps.utils.bridge_engine import execute_query

def get_pending_orders():
    """
    جلب الطلبات مباشرة من المحرك المركزي لقمرة.
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
    
    # تصفية الحالات المعلقة في الذاكرة
    return [o for o in orders if o.get('status') == 'pending']
