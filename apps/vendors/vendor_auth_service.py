# coding: utf-8
# 📂 apps/vendors/vendor_auth_service.py

import requests
import re
import os

class VendorAuthService:
    @staticmethod
    def initiate_login(phone, otp_code):
        """
        إرسال رمز التحقق عبر واتساب بأسلوب شخصي وودي.
        """
        # تنظيف الرقم والتأكد من وجود مفتاح الدولة
        clean_phone = re.sub(r'[^\d]', '', str(phone))
        if not clean_phone.startswith('+'):
            clean_phone = "+" + clean_phone
        
        # المفتاح من متغيرات البيئة أو القيمة الافتراضية
        api_key = os.environ.get('TEXTMEBOT_API_KEY', 'rb3tZFnHRcsN')
        
        # الرسالة بصيغة شخصية ومهنية
        message = (
            f"أهلاً بك يا شريكنا في محجوب أونلاين.\n\n"
            f"رمز التحقق الخاص بك للدخول هو: *{otp_code}*\n\n"
            f"يرجى استخدامه خلال 5 دقائق.\n\n"
            f"تحياتي،\n"
            f"إدارة محجوب أونلاين."
        )
        
        base_url = "http://api.textmebot.com/send.php"
        params = {
            "recipient": clean_phone,
            "apikey": api_key,
            "text": message,
            "json": "yes"
        }
        
        try:
            # إرسال الطلب
            response = requests.get(base_url, params=params, timeout=15)
            
            # تسجيل الاستجابة للتحقق من الحالة (لأغراض التطوير)
            print(f"DEBUG [TextMeBot Response]: {response.status_code} - {response.text}")
            
            # التأكد من النجاح
            return response.status_code == 200
            
        except Exception as e:
            # تسجيل أي خطأ في الاتصال
            print(f"CRITICAL [TextMeBot Error]: {e}")
            return False
