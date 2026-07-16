# coding: utf-8
# 📂 apps/services/graphql_client.py

import requests
import os
import logging
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# تعطيل تحذيرات الـ SSL إذا كانت الشهادات ذاتية التوقيع في البيئة المحلية
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class QomrahGraphQLClient:
    """
    كلاس موحد لإدارة طلبات GraphQL إلى API الخاص بـ 'محجوب'
    يتم استخدام هذا الكلاس كـ Proxy وسيط لضمان الأمان وتجاوز مشاكل الاتصال.
    """
    
    BASE_URL = "https://mahjoub.online/admin/graphql"
    
    @staticmethod
    def _get_session():
        """إعداد جلسة طلبات مع استراتيجية إعادة المحاولة عند الفشل."""
        session = requests.Session()
        # إعدادات إعادة المحاولة للتعامل مع أخطاء الشبكة المؤقتة
        retry_strategy = Retry(
            total=3,  # عدد مرات إعادة المحاولة
            backoff_factor=1,  # فترة الانتظار بين المحاولات
            status_forcelist=[429, 500, 502, 503, 504], # حالات الخطأ التي تستدعي إعادة المحاولة
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        return session

    @staticmethod
    def execute_query(query, variables=None):
        """تنفيذ استعلام GraphQL وإرجاع البيانات فقط."""
        api_key = os.environ.get('QUMRA_API_KEY')
        
        # التأكد من وجود مفتاح API
        if not api_key:
            logging.error("❌ مفتاح API غير موجود في إعدادات البيئة (QUMRA_API_KEY)")
            return None

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }
        
        session = QomrahGraphQLClient._get_session()
        try:
            response = session.post(
                QomrahGraphQLClient.BASE_URL,
                json={'query': query, 'variables': variables},
                headers=headers,
                verify=False, # التعديل هنا للعمل مع الروابط المحمية داخلياً
                timeout=30    # زيادة وقت الانتظار لتفادي انقطاع الاتصال
            )
            
            # التحقق من نجاح الرد (رفع استثناء في حال أخطاء 4xx أو 5xx)
            response.raise_for_status()
            
            result = response.json()
            
            # معالجة أخطاء GraphQL البرمجية (داخل الـ JSON نفسه)
            if 'errors' in result:
                logging.error(f"GraphQL API Errors: {result['errors']}")
                return None
                
            return result.get('data')
            
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ خطأ في الاتصال بـ {QomrahGraphQLClient.BASE_URL}: {str(e)}")
            return None
        except Exception as e:
            logging.error(f"❌ خطأ غير متوقع: {str(e)}")
            return None
