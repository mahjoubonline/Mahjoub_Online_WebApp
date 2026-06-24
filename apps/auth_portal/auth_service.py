# coding: utf-8
# 📂 apps/auth_portal/auth_service.py - النسخة المطابقة للتوثيق الرسمي

import os
import requests

class AdminAuthService:
    @staticmethod
    def initiate_login(phone, otp_code):
        # 1. جلب المفاتيح (الـ api_token هو نفسه المفتاح الذي أرفقت صورته)
        api_key = os.environ.get('HYPERSEND_API_KEY')
        
        # 2. تنظيف الرقم وتجهيزه للصيغة التي تتطلبها WhatsApp API
        clean_phone = "".join(filter(str.isdigit, str(phone)))
        if not clean_phone.startswith('967'):
            clean_phone = '967' + clean_phone.lstrip('0')
        
        # التنسيق المطلوب هو رقم الهاتف متبوعاً بـ @c.us
        chat_id = f"{clean_phone}@c.us"
        
        # 3. الرابط الصحيح (Endpoint) حسب توثيق HyperSender في Postman
        url = "https://app.hypersender.com/api/whatsapp/v1/instance/send-text"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 4. هيكل الرسالة (Payload) حسب توثيق Postman
        payload = {
            "chatId": chat_id,
            "text": f"رمز الدخول لمحجوب أونلاين هو: {otp_code}"
        }

        try:
            # 5. تنفيذ الطلب
            print(f"DEBUG: محاولة الاتصال بـ {url}")
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            
            # تحليل النتيجة
            print(f"DEBUG: Status Code: {response.status_code}")
            
            if response.status_code in [200, 201]:
                print("✅ نجاح: تم إرسال الرمز بنجاح.")
                return True
            else:
                # طباعة تفاصيل الخطأ للتشخيص
                print(f"CRITICAL: HyperSender Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"CRITICAL: فشل الاتصال: {str(e)}")
            return False
