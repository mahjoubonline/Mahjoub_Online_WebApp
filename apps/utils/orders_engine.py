# 📂 apps/utils/orders_engine.py
from apps.extensions import db
from apps.models.order_db import Order
import requests
import logging

logger = logging.getLogger(__name__)

class OrdersEngine:
    def __init__(self):
        self.api_url = "https://mahjoub.online/admin/graphql"
        self.api_key = "qmr_e063f7f4-ed44-4c86-b105-8405326b9eb9"
        # تم التأكد من صيغة Bearer كما طلبت
        self.headers = {
            "Authorization": f"Bearer {self.api_key}", 
            "Content-Type": "application/json"
        }

    def fetch_orders_from_qumra(self):
        print("DEBUG: بدء عملية استكشاف الـ Schema الحقيقية للحقول...")
        # هذا الاستعلام هو المفتاح، سيجلب لنا قائمة بكل الحقول المتاحة في كائن الطلب
        payload = {
            "query": """
            query {
                __type(name: "Order") {
                    fields {
                        name
                        type {
                            name
                            kind
                        }
                    }
                }
            }
            """
        }
        try:
            response = requests.post(self.api_url, json=payload, headers=self.headers, timeout=15)
            result = response.json()
            
            # طباعة خريطة الحقول في الـ Logs - هذا هو المرجع الذي سنبني عليه
            print(f"DEBUG: خريطة الحقول المتاحة (الرد الخام): {result}")
            
            return [] 
        except Exception as e:
            print(f"DEBUG: خطأ في الاستكشاف: {str(e)}")
            return []

    def sync_orders_to_db(self):
        print("DEBUG: بدء عملية المزامنة...")
        # تنفيذ عملية الاستكشاف
        self.fetch_orders_from_qumra()
        
        print("DEBUG: انتهت مرحلة الاستكشاف. يرجى مراجعة الـ Logs.")
