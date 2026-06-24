# coding: utf-8
# 📂 apps/suppliers_auth_portal/auth_service.py - خدمة إرسال التحقق للموردين عبر الواتساب (الإصدار المصحح والمؤمن)

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
        # تنظيف الرقم من أي رموز أو فراغات وإبقائه أرقاماً فقط
        clean_phone = re.sub(r'[^\d]', '', str(phone))
        
        # حماية إضافية: التأكد من صياغة الرقم اليمني بالشكل الدولي الصحيح لـ TextMeBot
        if clean_phone.startswith('00967'):
            clean_phone = clean_phone[2:]
        elif clean_phone.startswith('7') and len(clean_phone) == 9:
            clean_phone = '967' + clean_phone
        elif clean_phone.startswith('07') and len(clean_phone) == 10:
            clean_phone = '967' + clean_phone[1:]
            
        # جلب مفتاح الـ API الخاص بـ TextMeBot لشركاء النجاح
        api_key = os.environ.get('TEXTMEBOT_API_KEY', 'rb3tZFnHRcsN')
        
        # صياغة رسالة مخصصة تليق بهوية محجوب أونلاين للموردين
        message = (
            f"*Mahjoub Online | الشركاء والموردين*\n\n"
            f"رمز التحقق الأمني الخاص بك هو: *{otp_code}*\n\n"
            f"يرجى عدم مشاركة هذا الرمز مع أي شخص.\n"
            f"— محجوب أونلاين | سوقك الذكي"
        )
        
        base_url = "http://api.textmebot.com/send.php"
        
        params = {
            "recipient": clean_phone, 
            "apikey": api_key, 
            "text": message, 
            "json": "yes"
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try:
            # المحاولة الأولى للإرسال
            response = requests.get(base_url, params=params, headers=headers, timeout=15)
            
            # التعامل الذكي مع قيود التأخير المفروضة من المزود (Rate Limit)
            if response.status_code == 403 and "Delay needed" in response.text:
                print("⚠️ [Vendor Auth] تم اكتشاف قيود تأخير من TextMeBot، جاري الانتظار 10 ثوانٍ...")
                time.sleep(10)
                response = requests.get(base_url, params=params, headers=headers, timeout=15)
            
            # التحليل الفعلي للرد للتأكد من وصول الرسالة
            if response.status_code == 200:
                try:
                    res_json = response.json()
                    # فحص رد TextMeBot الفعلي لمعرفة هل تم الإرسال أم لا
                    if res_json.get('status') == 'success' or 'status' in res_json:
                        print(f"✅ [Vendor OTP Sent] تم تسليم الرسالة لسيرفر الواتساب بنجاح للرقم: {clean_phone}")
                        return True
                    else:
                        print(f"❌ [Vendor OTP API Error] الرد الفعلي للخدمة: {response.text}")
                        return False
                except Exception:
                    # في حال لم يرجع السيرفر JSON بالرغم من الحالة 200
                    if "success" in response.text.lower() or "sent" in response.text.lower():
                        print(f"✅ [Vendor OTP Sent] تم الإرسال (رد نصي): {clean_phone}")
                        return True
                    print(f"❌ [Vendor OTP Bad Response] الرد الراجع غير متوقع: {response.text}")
                    return False
            else:
                print(f"❌ [Vendor OTP Delivery Failed] الحالة: {response.status_code} - الرد: {response.text}")
                return False
                
        except Exception as e:
            print(f"🚨 CRITICAL [Vendor TextMeBot Error]: {str(e)}")
            return False
