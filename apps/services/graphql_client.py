# coding: utf-8
import requests
import logging
from config import Config

logger = logging.getLogger(__name__)

class QomrahGraphQLClient:
    @staticmethod
    def _get_headers():
        return {
            "Authorization": f"Bearer {Config.QUMRA_API_KEY}",
            "Content-Type": "application/json",
            "x-apollo-operation-name": "GetOrders",
            "apollo-require-preflight": "true"
        }

    @staticmethod
    def fetch_orders(headers=None):
        current_headers = headers if headers is not None else QomrahGraphQLClient._get_headers()
        
        # تم تعديل الحقول بناءً على رسالة الخطأ من السيرفر
        query = """
        query GetOrders {
          findAllOrders { 
            data {
              _id
              totalPrice
              status {
                # السيرفر اشتكى من name، جربنا تغييرها إلى ما هو شائع في Apollo أو تركها فارغة إذا لم نعرف
                # لكن بناءً على الخطأ، السيرفر لا يعرف name هنا. 
                # سنحاول جلب الحقل الأساسي فقط حالياً:
              }
              createdAt
              items {
                productData { # السيرفر اقترح productData
                  name
                }
                quantity
                price
                # السيرفر اشتكى من sku، سنحذفه حالياً حتى نتأكد من وجوده في الـ Schema
              }
            }
          }
        }
        """
        
        try:
            payload = {'query': query, 'operationName': 'GetOrders'}
            response = requests.post(Config.QUMRA_API_URL, json=payload, headers=current_headers, timeout=15)
            response.raise_for_status()
            result = response.json()
            return result.get('data', {}).get('findAllOrders', {}).get('data', [])
        except Exception as e:
            logger.error(f"❌ خطأ في الاتصال: {e}")
            return []
