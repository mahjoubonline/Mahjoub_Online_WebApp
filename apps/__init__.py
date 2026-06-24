# coding: utf-8
# 📂 apps/auth_portal/auth_service.py - محرك إرسال الرموز (إصدار V2 المحسن للخطة المجانية)

import os
import requests
import time

class AdminAuthService:
    @staticmethod
    def initiate_login(phone, otp_code, retries=3):
        """
        إرسال الرمز عبر خدمة الرسائل المباشرة متوافقة مع V2 و Instance ID.
        """
        # سحب البيانات من متغيرات البيئة في Render
        api_key = os.environ.get('HYPERSEND_API_KEY')
        instance_id = os.environ.get('HYPERSEND_INSTANCE_ID')
        
        # تنظيف الرقم
        clean_phone = "".join(filter(str.isdigit, str(phone)))
        if not clean_phone.startswith('967'):
            clean_phone = '967' + clean_phone.lstrip('0')
        
        chat_id = f"{clean_phone}@c.us"
        
        # الرابط المعتمد لإرسال الرسائل في V2 مع الـ Instance ID
        # تم تصحيح المسار ليكون متوافقاً مع هيكلية الـ API للرسائل
        url = f"https://app.hypersender.com/api/v2/instance/{instance_id}/messages/chat"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # هيكل الرسالة
        payload = {
            "chatId": chat_id,
            "contentType": "string",
            "content": f"رمز الدخول الخاص بك لمحجوب أونلاين هو: {otp_code}"
        }

        print(f"DEBUG: محاولة إرسال رسالة إلى {chat_id} عبر Instance: {instance_id}")

        for attempt in range(retries):
            try:
                response = requests.post(url, json=payload, headers=headers, timeout=15)
                
                # التحقق من نجاح العملية (كود 200 أو 201)
                if response.status_code in [200, 201]:
                    print("✅ [Admin OTP] تم إرسال الرمز بنجاح.")
                    return True
                else:
                    print(f"DEBUG: فشل الإرسال (محاولة {attempt+1}) - كود {response.status_code}: {response.text}")
            
            except Exception as e:
                print(f"🚨 [Admin Error]: {str(e)}")
            
            # انتظار قصير قبل إعادة المحاولة
            time.sleep(2)

        return False
