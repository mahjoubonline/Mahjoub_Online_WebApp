# coding: utf-8
# 📂 apps/services/graphql_client.py - عميل الاتصال بـ Qomrah API

import requests
import logging
from config import Config

logger = logging.getLogger(__name__)

class QomrahGraphQLClient:
    """عميل متخصص لجلب بيانات الطلبات من منصة قمرة."""

    @staticmethod
    def _get_headers():
        return {
            "Authorization": f"Bearer {Config.QUMRA_API_KEY}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def fetch_orders(limit=20, offset=0):
        """
        جلب قائمة الطلبات باستخدام صيغة Qomrah Analytics Query.
        """
        # استخدام الاستعلام الأساسي مع خاصية الترقيم
        query = f"QUERY orders LIMIT {limit} OFFSET {offset}"
        
        try:
            response = requests.post(
                Config.QUMRA_API_URL, 
                json={'query': query},
                headers=QomrahGraphQLClient._get_headers(),
                timeout=15
            )
            response.raise_for_status()
            result = response.json()
            
            # إرجاع البيانات المطلوبة
            return result.get('data', [])
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ خطأ في الاتصال بسيرفر قمرة عند جلب قائمة الطلبات: {e}")
            return []

    @staticmethod
    def get_order_details(order_id):
        """
        جلب تفاصيل طلب محدد.
        (ملاحظة: إذا كانت قمرة تتطلب QUERY مخصصاً، استبدل الاستعلام أدناه)
        """
        query = f"QUERY orders FILTER id = {order_id}"
        
        try:
            response = requests.post(
                Config.QUMRA_API_URL, 
                json={'query': query},
                headers=QomrahGraphQLClient._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            data = result.get('data', [])
            return data[0] if isinstance(data, list) and len(data) > 0 else None

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ خطأ في الاتصال بسيرفر قمرة عند جلب الطلب {order_id}: {e}")
            return None
