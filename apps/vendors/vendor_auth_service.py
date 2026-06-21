import requests
import re
from flask import current_app

class VendorAuthService:
    @staticmethod
    def initiate_login(phone, otp_code):
        # 1. تنظيف الرقم (يجب أن يبدأ بـ + كما هو موضح في مثال الموقع)
        clean_phone = re.sub(r'[^\d]', '', str(phone))
        if not clean_phone.startswith('+'):
            clean_phone = "+" + clean_phone
        
        # 2. البيانات الخاصة بحسابك من textmebot
        # يفضل وضع هذه القيم في ملف .env في Render
        api_key = "rb3tZFnHRcsN" 
        
        # 3. بناء الرابط حسب توثيق textmebot
        # الرابط: http://api.textmebot.com/send.php?recipient=[phone]&apikey=[key]&text=[text]
        base_url = "http://api.textmebot.com/send.php"
        message = f"رمز التحقق لمحجوب أونلاين هو: {otp_code}"
        
        params = {
            "recipient": clean_phone,
            "apikey": api_key,
            "text": message,
            "json": "yes" # لطلب رد بصيغة JSON كما هو موضح في توثيق الموقع
        }
        
        try:
            # إرسال الطلب عبر GET كما يطلب الموقع
            response = requests.get(base_url, params=params, timeout=10)
            
            # التحقق من نجاح العملية
            if response.status_code == 200:
                print(f"✅ [WhatsApp] تم إرسال الرمز بنجاح إلى {clean_phone}")
                return True
            else:
                print(f"⚠️ [WhatsApp Error] فشل الإرسال: {response.text}")
                return False
        except Exception as e:
            print(f"❌ [System Error] خطأ في الاتصال بـ textmebot: {e}")
            return False
