# 📂 apps/utils/orders_engine.py
import logging
from apps.utils.bridge_engine import execute_query

logger = logging.getLogger(__name__)

def get_pending_orders():
    # استعلام شامل للتحقق من هيكلية البيانات
    query = """
    query {
      findAllOrders {
        __typename
        items {
          id
          totalPrice
        }
      }
    }
    """
    try:
        result = execute_query(query)
        # هذا السطر سيطبع في سجلات Render كل ما يأتي من قمرة
        logger.info(f"DEBUG_DATA: {result}")
        
        return result.get('data', {}).get('findAllOrders', {}).get('items', [])
    except Exception as e:
        logger.error(f"Error: {e}")
        return []
