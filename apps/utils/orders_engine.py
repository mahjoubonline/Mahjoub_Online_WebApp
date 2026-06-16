# 📂 apps/utils/orders_engine.py
import logging
from apps.utils.bridge_engine import execute_query

logger = logging.getLogger(__name__)

def get_pending_orders():
    """
    جلب الطلبات المعلقة مع معالجة أخطاء قوية لتجنب توقف النظام.
    """
    # تعديل الاستعلام ليكون أكثر دقة أو مرونة إذا لزم الأمر
    query = """
    query {
      pendingOrders {
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
        
        # تسجيل النتيجة للتشخيص في حال وجود خطأ
        if not result or 'data' not in result:
            logger.warning(f"Qumra API returned empty or error: {result}")
            return []
            
        # نعتمد على أن الحقل قد يكون 'pendingOrders' أو 'orders' حسب API قمرة
        data = result.get('data', {})
        return data.get('pendingOrders') or data.get('orders', [])

    except Exception as e:
        logger.error(f"Critical error in get_pending_orders: {str(e)}")
        # إرجاع قائمة فارغة لمنع حدوث خطأ 500 للمستخدم
        return []
