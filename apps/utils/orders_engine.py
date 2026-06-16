# 📂 apps/utils/orders_engine.py
import logging
from apps.utils.bridge_engine import execute_query

logger = logging.getLogger(__name__)

def get_pending_orders():
    """
    جلب الطلبات المعلقة باستخدام اسم الاستعلام الصحيح (findAllOrders) 
    الذي يدعمه API قمرة.
    """
    # استخدام findAllOrders بناءً على اقتراح الـ API في الـ Logs
    query = """
    query {
      findAllOrders(status: "pending") {
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
    """
    try:
        result = execute_query(query)
        
        # التأكد من وجود البيانات
        if not result or 'data' not in result:
            logger.warning(f"Qumra API returned empty or error: {result}")
            return []
            
        # استخراج البيانات باستخدام findAllOrders كأولوية
        data = result.get('data', {})
        
        # نتحقق من الحقل الصحيح في الاستجابة
        orders = data.get('findAllOrders') or data.get('orders', [])
        return orders

    except Exception as e:
        logger.error(f"Critical error in get_pending_orders: {str(e)}")
        # إرجاع قائمة فارغة لمنع حدوث خطأ 500 للمستخدم
        return []
