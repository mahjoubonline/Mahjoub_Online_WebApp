import requests
from apps.models.otp_db import OTPVerification

class VendorAuthService:
    API_KEY = "rb3tZFnHRcsN" # المفتاح الذي ظهر في الصورة
    
    @staticmethod
    def send_whatsapp_otp(phone_number, otp_code):
        """إرسال الكود عبر واتساب باستخدام API المورد"""
        message = f"مرحباً، رمز التحقق الخاص بك لبوابة الموردين هو: {otp_code}"
        # تشفير الرسالة لتناسب الـ URL
        encoded_message = requests.utils.quote(message)
        
        # الرابط بناءً على صيغة الـ API التي أرسلتها
        url = f"http://api.textmebot.com/send.php?recipient={phone_number}&apikey={VendorAuthService.API_KEY}&text={encoded_message}"
        
        try:
            response = requests.get(url)
            return response.status_code == 200
        except Exception as e:
            print(f"Error sending WhatsApp: {e}")
            return False

    @staticmethod
    def initiate_login(phone):
        """بدء عملية الدخول: توليد كود وإرساله"""
        # 1. توليد كود وتخزينه
        otp = OTPVerification.generate_otp(phone)
        
        # 2. إرسال الكود
        success = VendorAuthService.send_whatsapp_otp(phone, otp)
        return success
