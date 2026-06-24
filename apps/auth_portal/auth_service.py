# coding: utf-8
# 📂 apps/auth_portal/auth_service.py - محرك إرسال الرموز (الإصدار التوافقي النهائي)

import os
import requests
import time

class AdminAuthService:
    @staticmethod
    def initiate_login(phone, otp_code, retries=3):
        """
        محرك إرسال رسائل ذكي يدعم مسارين للـ API لتجاوز أخطاء الـ 404.
        """
        api_key = os.environ.get('HYPERSEND_API_KEY')
        instance_id = os.environ.get('HYPERSEND_INSTANCE_ID')
        
        # تنظيف الرقم
        clean_phone = "".join(filter(str.isdigit, str(phone)))
        if not clean_phone.startswith('967'):
            clean_phone = '967' + clean_phone.lstrip('0')
        
        # قائمة المسارات المحتملة للـ API (يتم تجربة الأول، ثم الثاني في حال الفشل)
        endpoints = [
            {
                "url": f"https://app.hypersender.com/api/v1/instance/{instance_id}/message",
                "payload": {
                    "number": f"{clean_phone}@c.us",
                    "type": "text",
                    "message": f"رمز الدخول لمحجوب أونلاين هو: {otp_code}"
                }
            },
            {
                "url": "https://api.hypersender.com/v1/messages/send",
                "payload": {
                    "instance": instance_id,
                    "to": f"{clean_phone}@c.us",
                    "text": f"رمز الدخول لمحجوب أونلاين هو: {otp_code}"
                }
            }
        ]

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        for attempt in range(retries):
            # تجربة المسارات المتوفرة
            for ep in endpoints:
                try:
                    print(f"DEBUG: محاولة إرسال عبر المسار: {ep['url']}")
                    response = requests.post(ep['url'], json=ep['payload'], headers=headers, timeout=15)
                    
                    if response.status_code == 200:
                        print("✅ [Admin OTP] تم الإرسال بنجاح.")
                        return True
                    else:
                        print(f"DEBUG: المسار {ep['url']} فشل (كود {response.status_code}): {response.text}")
                
                except Exception as e:
                    print(f"🚨 [Admin Error]: {str(e)}")
            
            time.sleep(2)

        return False
