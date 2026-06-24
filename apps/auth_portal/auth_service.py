# coding: utf-8
# 📂 apps/auth_portal/auth_service.py - محرك إرسال الرموز (الإصدار التوافقي الموحد)

import os
import requests
import time

class AdminAuthService:
    @staticmethod
    def initiate_login(phone, otp_code, retries=3):
        api_key = os.environ.get('HYPERSEND_API_KEY')
        instance_id = os.environ.get('HYPERSEND_INSTANCE_ID')
        
        # تنظيف الرقم
        clean_phone = "".join(filter(str.isdigit, str(phone)))
        if not clean_phone.startswith('967'):
            clean_phone = '967' + clean_phone.lstrip('0')
        
        # الرابط الموحد للخطط (V1) - هذا المسار هو الأكثر قبولاً لدى الخوادم
        url = f"https://app.hypersender.com/api/v1/instance/{instance_id}/message"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # استخدام المفاتيح القياسية (number, type, message)
        payload = {
            "number": f"{clean_phone}@c.us",
            "type": "text",
            "message": f"رمز الدخول الخاص بك لمحجوب أونلاين هو: {otp_code}"
        }

        print(f"DEBUG: محاولة إرسال رسالة إلى {clean_phone} عبر الرابط: {url}")

        for attempt in range(retries):
            try:
                response = requests.post(url, json=payload, headers=headers, timeout=15)
                
                # طباعة الرد بالتفصيل في حال الفشل
                if response.status_code == 200:
                    print("✅ [Admin OTP] تم إرسال الرمز بنجاح.")
                    return True
                else:
                    print(f"DEBUG: فشل الإرسال (محاولة {attempt+1}) - كود {response.status_code}: {response.text}")
            
            except Exception as e:
                print(f"🚨 [Admin Error]: {str(e)}")
            
            time.sleep(2)

        return False
