# coding: utf-8
# 📂 apps/suppliers_auth_portal/auth_service.py - خدمة إرسال التحقق للموردين عبر الواتساب

import os
import re
import time
import requests

class VendorAuthService:
    @staticmethod
    def initiate_login(phone, otp_code):
        """
        إرسال رمز التحقق الـ OTP الخاص بالموردين والمسوقين عبر خدمة TextMeBot (WhatsApp).
        """
        clean_phone = re.sub(r'[^\d]', '', str(phone))
        
        # جلب مفتاح الـ API الخاص بـ TextMeBot لشركاء النجاح
        api_key = os.environ.get('TEXTMEBOT_API_KEY', 'rb3tZFnHRcsN')
        
        # صياغة رسالة مخصصة تليق بهوية محجوب أونلاين للموردين
        message = f"Mahjoub Online | الشركاء والموردين\n\nرمز التحقق الأمني الخاص بك هو: {otp_code}\n\nيرجى عدم مشاركة هذا الرمز مع أي شخص.\n— محجوب أونلاين | سوقك الذكي"
        base_url = "http://api.textmebot.com/send.php"
        
        params = {
            "recipient": clean_phone, 
            "apikey": api_key, 
            "text": message, 
            "json": "yes"
        }
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        try:
            # المحاولة الأولى للإرسال
            response = requests.get(base_url, params=params, headers=headers, timeout=15)
            
            # التعامل الذكي مع قيود التأخير المفروضة من المزود (Rate Limit)
            if response.status_code == 403 and "Delay needed" in str(response.text):
                print("⚠️ [Vendor Auth] تم اكتشاف قيود تأخير من TextMeBot، جاري الانتظار 10 ثوانٍ...")
                time.sleep(10)
                # إعادة المحاولة بعد الانتظار
                response = requests.get(base_url, params=params, headers=headers, timeout=15)
            
            # التحقق من نجاح العملية
            if response.status_code == 200:
                print(f"✅ [Vendor OTP Sent] تم إرسال الرمز بنجاح للمورد على الرقم: {clean_phone}")
                return True
            else:
                print(f"❌ [Vendor OTP Delivery Failed] الحالة: {response.status_code} - الرد: {response.text}")
                return False
                
        except Exception as e:
            print(f"🚨 CRITICAL [Vendor TextMeBot Error]: {str(e)}")
            return False
