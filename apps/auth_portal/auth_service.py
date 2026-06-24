# coding: utf-8
# 📂 apps/auth_portal/auth_service.py - النسخة المصححة تقنياً

import os
import requests

class AdminAuthService:
    @staticmethod
    def initiate_login(phone, otp_code):
        # سحب البيانات من متغيرات البيئة
        api_key = os.environ.get('HYPERSEND_API_KEY')
        instance_id = os.environ.get('HYPERSEND_INSTANCE_ID')
        
        # تنظيف الرقم (تنسيق دولي)
        clean_phone = "".join(filter(str.isdigit, str(phone)))
        if not clean_phone.startswith('967'):
            clean_phone = '967' + clean_phone.lstrip('0')
        
        # المسار المعدل (جرب هذا المسار، فهو الأكثر شيوعاً في API V1)
        url = f"https://app.hypersender.com/api/v1/instance/{instance_id}/message/text"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "number": clean_phone,
            "message": f"رمز الدخول لمحجوب أونلاين هو: {otp_code}"
        }

        try:
            print(f"DEBUG: محاولة إرسال لـ {clean_phone} على الرابط {url}")
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code in [200, 201]:
                return True
            else:
                # هذا السطر سيخبرنا في الـ Logs بالضبط لماذا رفض السيرفر الطلب
                print(f"CRITICAL: HyperSender Error {response.status_code}: {response.text}")
                return False
        except Exception as e:
            print(f"CRITICAL: Connection Error: {str(e)}")
            return False
