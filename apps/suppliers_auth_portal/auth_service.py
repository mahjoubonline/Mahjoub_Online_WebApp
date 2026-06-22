# coding: utf-8
# 📂 apps/suppliers_auth_portal/auth_service.py

import requests
import re
import os

class VendorAuthService:
    """
    خدمة التحقق الخاصة بالموردين عبر واتساب (TextMeBot)
    """
    
    @staticmethod
    def initiate_login(phone, otp_code):
        # 1. تنظيف الرقم من أي رموز لضمان توافقه مع الـ API
        clean_phone = re.sub(r'[^\d]', '', str(phone))
        
        # 2. جلب المفتاح من متغيرات البيئة (الأكثر أماناً)
        api_key = os.environ.get('TEXTMEBOT_API_KEY', 'rb3tZFnHRcsN')
        
        # 3. صياغة الرسالة (تجنب الرموز المعقدة لضمان التوافق)
        message = (
            f"Mahjoub Online | Security Code\n\n"
            f"أهلاً بك يا شريك النجاح.\n"
            f"رمز التحقق لدخولكم هو:\n\n"
            f"{otp_code}\n\n"
            f"صلاحية الرمز 5 دقائق.\n"
            f"— محجوب أونلاين"
        )
        
        base_url = "http://api.textmebot.com/send.php"
        
        # 4. إعداد المعاملات
        params = {
            "recipient": clean_phone, 
            "apikey": api_key,
            "text": message,
            "json": "yes"
        }
        
        try:
            # 5. إرسال الطلب مع مهلة زمنية (Timeout) لتجنب تعليق النظام
            response = requests.get(base_url, params=params, timeout=15)
            
            # تسجيل الاستجابة (مفيد جداً في الـ Logs لتصحيح الأخطاء)
            print(f"DEBUG [TextMeBot Response]: {response.status_code} - {response.text}")
            
            # 6. التحقق من النجاح
            return response.status_code == 200
            
        except Exception as e:
            # تسجيل الخطأ في الـ Logs
            print(f"CRITICAL [TextMeBot Error]: {str(e)}")
            return False
