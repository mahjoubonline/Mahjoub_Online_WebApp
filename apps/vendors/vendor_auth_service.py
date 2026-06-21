# 📂 apps/vendors/vendor_auth_service.py
import requests
from apps.models.otp_db import OTPVerification

class VendorAuthService:
    API_KEY = "rb3tZFnHRcsN" 
    
    @staticmethod
    def send_whatsapp_otp(phone_number, otp_code):
        """إرسال الكود عبر واتساب مع تنظيف الرقم من الرموز"""
        # تنظيف الرقم: إزالة أي مسافات أو علامة "+" لضمان قبول الـ URL
        clean_phone = phone_number.replace("+", "").replace(" ", "")
        
        message = f"مرحباً، رمز التحقق لبوابة محجوب أونلاين هو: {otp_code}"
        # تشفير الرسالة لتناسب الـ URL (تحويل المسافات والرموز العربية)
        encoded_message = requests.utils.quote(message)
        
        url = f"http://api.textmebot.com/send.php?recipient={clean_phone}&apikey={VendorAuthService.API_KEY}&text={encoded_message}"
        
        try:
            # إضافة timeout لتجنب تعليق السيرفر في حال تأخر استجابة الـ API
            response = requests.get(url, timeout=10)
            
            # طباعة الحالة في سجلات Render لمراقبة أي مشكلة مستقبلية
            print(f"TextMeBot Response: {response.status_code} - {response.text}")
            
            # التحقق من أن الـ API استجاب بنجاح
            return response.status_code == 200
        except Exception as e:
            # في حال حدوث خطأ في الاتصال، يتم تسجيله دون إيقاف التطبيق
            print(f"Error sending WhatsApp: {e}")
            return False

    @staticmethod
    def initiate_login(phone):
        """بدء عملية الدخول: توليد كود وإرساله"""
        # 1. توليد كود وتخزينه في قاعدة البيانات
        otp = OTPVerification.generate_otp(phone)
        
        if not otp:
            return False
            
        # 2. إرسال الكود
        return VendorAuthService.send_whatsapp_otp(phone, otp)
