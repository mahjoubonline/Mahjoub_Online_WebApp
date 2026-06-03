# 📂 apps/utils/whatsapp/api_client.py
import requests
import os

class WhatsAppClient:
    def __init__(self):
        self.api_url = f"https://graph.facebook.com/v20.0/{os.environ.get('PHONE_NUMBER_ID')}/messages"
        self.headers = {
            "Authorization": f"Bearer {os.environ.get('WHATSAPP_TOKEN')}",
            "Content-Type": "application/json"
        }

    def send_message(self, recipient_phone, template_name, language="ar"):
        """دالة عامة لإرسال الرسائل عبر قوالب ميتا"""
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_phone,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language}
            }
        }
        response = requests.post(self.api_url, json=payload, headers=self.headers)
        return response.json()
