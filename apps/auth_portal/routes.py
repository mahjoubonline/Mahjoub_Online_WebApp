# coding: utf-8
# 📂 apps/auth_portal/auth_service.py - النسخة النهائية المطابقة للتوثيق

import os
import requests

class AdminAuthService:
    @staticmethod
    def initiate_login(phone, otp_code):
        api_key = os.environ.get('HYPERSEND_API_KEY')
        
        # 1. تنظيف الرقم (بدون أي مسافات)
        clean_phone = "".join(filter(str.isdigit, str(phone)))
        if not clean_phone.startswith('967'):
            clean_phone = '967' + clean_phone.lstrip('0')
        
        # 2. التنسيق الدقيق المطلوب لـ HyperSender
        chat_id = f"{clean_phone}@c.us"
        
        # 3. الرابط المعتمد من توثيق Postman
        url = "https://app.hypersender.com/api/whatsapp/v1/instance/send-text"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 4. الـ Payload الدقيق (مطابق لصور Postman)
        payload = {
            "chatId": chat_id,
            "text": f"رمز الدخول لمحجوب أونلاين هو: {otp_code}"
        }

        try:
            print(f"DEBUG: محاولة الإرسال لـ {chat_id}")
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            
            if response.status_code in [200, 201]:
                return True
            else:
                print(f"CRITICAL: HyperSender Error: {response.text}")
                return False
        except Exception as e:
            print(f"CRITICAL: Connection Error: {str(e)}")
            return False
