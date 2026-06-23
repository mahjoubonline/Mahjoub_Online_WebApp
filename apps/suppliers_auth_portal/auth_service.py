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
        # 1. تنظيف الرقم (إزالة أي شيء ليس رقماً لضمان التنسيق الدولي الصحيح)
        clean_phone = re.sub(r'[^\d]', '', str(phone))
        
        # 2. جلب المفتاح من متغيرات البيئة
        api_key = os.environ.get('TEXTMEBOT_API_KEY', 'rb3tZFnHRcsN')
        
        # 3. صياغة الرسالة
        message = (
            f"Mahjoub Online | Security Code\n\n"
            f"أهلاً بك يا شريك النجاح.\n"
            f"رمز التحقق لدخولكم هو: {otp_code}\n\n"
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
        
        # 5. إضافة هيدر المتصفح لتجاوز الحظر
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        try:
            # إرسال الطلب مع مهلة زمنية 15 ثانية
            response = requests.get(base_url, params=params, headers=headers, timeout=15)
            
            # تسجيل الاستجابة بالكامل في الـ Logs
            print(f"DEBUG [TextMeBot Response]: {response.status_code} - {response.text}")
            
            # التحقق من أن الطلب نجح (حالة 200)
            if response.status_code == 200:
                # التحقق الإضافي: بعض الـ APIs تعيد 200 ولكن بداخلها خطأ في الـ JSON
                data = response.json() if 'json' in response.headers.get('Content-Type', '') else {}
                if data.get('status') == 'error':
                    print(f"⚠️ [TextMeBot API Error]: {data.get('message')}")
                    return False
                return True
            else:
                return False
            
        except Exception as e:
            # تسجيل أي خطأ تقني (مثل انقطاع الاتصال)
            print(f"CRITICAL [TextMeBot Error]: {str(e)}")
            return False
