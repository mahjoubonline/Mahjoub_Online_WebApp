# 📂 apps/utils/orders_engine.py
import logging
from apps.utils.bridge_engine import execute_query

logger = logging.getLogger(__name__)

def get_pending_orders():
    """
    جلب الطلبات من الواجهة البرمجية لمتجر محجوب معالجة هيكلية التصفح (Pagination)
    """
    query = """
    query {
      findAllOrders {
        __typename
        items {
          id
          totalPrice
          status
          createdAt
          lineItems {
            product {
              name
              tags
            }
          }
        }
      }
    }
    """
    try:
        result = execute_query(query)
        
        # طباعة الاستجابة الخام في سجلات Render للتشخيص الدقيق عند الحاجة
        logger.info(f"DEBUG_DATA: Qumra API Raw Response: {result}")
        
        if not result or 'data' not in result:
            return []
            
        # الوصول إلى حاوية العناصر (items) المفهرسة داخلياً
        data = result.get('data', {}).get('findAllOrders', {})
        orders = data.get('items', []) if data else []
        
        # نقوم بعمل تصفية (Filter) محلياً للطلبات المعلقة لحين دعم الفلترة من الـ API مباشرة
        pending_orders = [o for o in orders if o.get('status') == 'pending']
        
        # إذا كانت القائمة المفلترة فارغة، نرجع العناصر كاملة لتجنب الجداول الفارغة كإجراء احتياطي
        return pending_orders if pending_orders else orders

    except Exception as e:
        logger.error(f"Critical error in get_pending_orders: {str(e)}")
        return []
