# 📂 apps/utils/orders_engine.py
import logging
from apps.utils.bridge_engine import execute_query

# إعداد الـ logger
logger = logging.getLogger(__name__)

def get_pending_orders():
    """
    جلب الطلبات المعلقة مع تعديل الهيكلية لتناسب PaginatedOrdersResponse
    """
    # تمت إزالة الـ status من الاستعلام لأنها سببت خطأ
    # ونقوم بالوصول إلى الـ items بدلاً من المصفوفة المباشرة
    query = """
    query {
      findAllOrders {
        items {
          id
          totalPrice
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
        
        # [التشخيص] طباعة الاستجابة الخام في الـ Logs
        logger.info(f"DEBUG: Qumra API Raw Response: {result}")
        
        if not result or 'data' not in result:
            return []
            
        # الوصول للهيكل الجديد: findAllOrders -> items
        data = result.get('data', {}).get('findAllOrders', {})
        orders = data.get('items', [])
        
        # تصفية الطلبات المعلقة محلياً في بايثون
        # (بما أن الـ API لا يقبل status في الاستعلام)
        pending_orders = [o for o in orders if o.get('status') == 'pending']
        
        return pending_orders if pending_orders else orders

    except Exception as e:
        logger.error(f"Critical error in get_pending_orders: {str(e)}")
        return []
