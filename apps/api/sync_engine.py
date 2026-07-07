# coding: utf-8
# 📂 apps/services/graphql_client.py - النسخة المصححة بناءً على رسائل خطأ السيرفر

import requests
import logging
from config import Config

logger = logging.getLogger(__name__)

class QomrahGraphQLClient:
    """عميل متخصص لجلب بيانات الطلبات من منصة قمرة عبر GraphQL."""

    @staticmethod
    def _get_headers():
        return {
            "Authorization": f"Bearer {Config.QUMRA_API_KEY}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def fetch_orders(limit=20, offset=0):
        """جلب قائمة الطلبات باستخدام الحقول المكتشفة من السيرفر."""
        
        # تصحيح الاستعلام بناءً على رسائل الخطأ التي أرسلتها
        query = """
        query GetOrders {
          findAllOrders { 
            data {
              _id
              totalPrice
              status {
                name
              }
              createdAt
              items {
                productName
                quantity
                price
                sku
              }
            }
          }
        }
        """
        # ملاحظة: السيرفر اشتكى من limit/offset، لذا قد تكون هذه الدالة 
        # تعيد كل شيء أو تحتاج لطريقة ترقيم أخرى. سنبدأ بدونها.
        
        try:
            response = requests.post(
                Config.QUMRA_API_URL, 
                json={'query': query},
                headers=QomrahGraphQLClient._get_headers(),
                timeout=15
            )
            response.raise_for_status()
            result = response.json()
            
            return result.get('data', {}).get('findAllOrders', {}).get('data', [])
            
        except Exception as e:
            logger.error(f"❌ خطأ في الاتصال بـ GraphQL: {e}")
            return []
