import requests
import os
from flask import current_app

class QumraConnector:
    """
    محرك الربط مع منصة قمرة - Qumra API Engine
    المسؤول عن مزامنة المنتجات واستقبال الويب هوك.
    """
    def __init__(self):
        self.api_key = os.getenv('QUMRA_API_KEY')
        self.base_url = "https://api.qumra.com/v1" # تأكد من رابط الـ API الرسمي من وثائقهم
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def sync_product_to_qumra(self, product_data):
        """إرسال بيانات المنتج من لوحة المورد إلى متجر قمرة"""
        endpoint = f"{self.base_url}/products"
        try:
            response = requests.post(endpoint, json=product_data, headers=self.headers)
            if response.status_code in [200, 201]:
                return response.json()
            else:
                print(f"Error syncing to Qumra: {response.text}")
                return None
        except Exception as e:
            print(f"Exception during Qumra sync: {str(e)}")
            return None

    def get_order_details(self, order_id):
        """جلب تفاصيل الطلب لمعالجة العمولات والمحافظ الموردين"""
        endpoint = f"{self.base_url}/orders/{order_id}"
        response = requests.get(endpoint, headers=self.headers)
        return response.json() if response.status_code == 200 else None

    def verify_webhook(self, payload, signature):
        """التحقق من صحة إشارة الويب هوك القادمة من قمرة (للأمان السيادي)"""
        # هنا يتم وضع منطق التحقق باستخدام الـ Webhook Secret
        pass
