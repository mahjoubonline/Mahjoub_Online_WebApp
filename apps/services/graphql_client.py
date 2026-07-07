# coding: utf-8
# 📂 apps/services/graphql_client.py - النسخة النهائية المصححة

import requests
import logging
from config import Config

logger = logging.getLogger(__name__)

class QomrahGraphQLClient:
    """عميل متخصص لجلب بيانات الطلبات من منصة قمرة عبر GraphQL."""

    @staticmethod
    def _get_headers():
        """تحضير الترويسات مع إضافة الترويسات الأمنية لتجاوز CSRF"""
        return {
            "Authorization": f"Bearer {Config.QUMRA_API_KEY}",
            "Content-Type": "application/json",
            "x-apollo-operation-name": "GetOrders",
            "apollo-require-preflight": "true"
        }

    @staticmethod
    def fetch_orders():
        """جلب قائمة الطلبات باستخدام الهيكلية المكتشفة من السيرفر."""
        
        # الاستعلام مصحح ليتناسب مع Schema السيرفر (findAllOrders)
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
        
        try:
            response = requests.post(
                Config.QUMRA_API_URL, 
                json={'query': query},
                headers=QomrahGraphQLClient._get_headers(),
                timeout=15
            )
            response.raise_for_status()
            result = response.json()
            
            # استخراج البيانات بناءً على هيكلية الـ JSON المكتشفة
            return result.get('data', {}).get('findAllOrders', {}).get('data', [])
            
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"❌ خطأ HTTP أثناء الاتصال بـ GraphQL: {http_err}")
            return []
        except Exception as e:
            logger.error(f"❌ خطأ غير متوقع أثناء الاتصال بـ GraphQL: {e}")
            return []
