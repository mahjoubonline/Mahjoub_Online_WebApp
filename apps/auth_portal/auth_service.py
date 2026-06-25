# coding: utf-8
# 📂 apps/auth_portal/auth_service.py - النسخة النهائية المعدلة

import os
import requests

class AdminAuthService:
    @staticmethod
    def initiate_login(phone, otp_code):
        # 1. جلب الإعدادات من متغيرات البيئة
        api_key = os.environ.get('HYPERSEND_API_KEY')
        instance_id = os.environ.get('HYPERSEND_INSTANCE_ID')
        
        if not api_key or not instance_id:
            print("CRITICAL: Missing HYPERSEND_API_KEY or HYPERSEND_INSTANCE_ID")
            return False
        
        # 2. تنظيف الرقم
        clean_phone = "".join(filter(str.isdigit, str(phone)))
        if not clean_phone.startswith('967'):
            clean_phone = '967' + clean_phone.lstrip('0')
        chat_id = f"{clean_phone}@c.us"
        
        # 3. تعديل الرابط: إزالة /v1/ قد يحل مشكلة الـ 404 إذا لم تكن مدعومة
        # الرابط المعتمد: https://app.hypersender.com/api/whatsapp/instance/{id}/send-text
        url = f"https://app.hypersender.com/api/whatsapp/instance/{instance_id}/send-text"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # 4. الـ Payload
        payload = {
            "chatId": chat_id,
            "text": f"رمز الدخول لمحجوب أونلاين هو: {otp_code}"
        }

        try:
            print(f"DEBUG: URL Request: {url}")
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            
            if response.status_code in [200, 201]:
                print("✅ نجاح: تم إرسال الرمز بنجاح.")
                return True
            else:
                print(f"CRITICAL: HyperSender Error {response.status_code}")
                print(f"CRITICAL: Response Text: {response.text}")
                return False
        except Exception as e:
            print(f"CRITICAL: Connection Error: {str(e)}")
            return False
