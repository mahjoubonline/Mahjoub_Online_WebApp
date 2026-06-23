# coding: utf-8
# 📂 apps/auth_portal/auth_service.py - خدمة إرسال رموز الإدارة (Admin OTP Service)

import os
import requests
import re

class AdminAuthService:
    @staticmethod
    def initiate_login(phone, otp_code):
        """
        خدمة إرسال الرموز للإدارة. 
        يمكنك هنا استخدام بوابة مختلفة (مثل SMS) أو نفس بوابة الموردين.
        """
        try:
            # تنظيف الرقم
            clean_phone = re.sub(r'[^\d]', '', str(phone))
            
            # يمكنك استخدام API مختلف للإدارة لضمان عدم تعارض العمليات
            api_key = os.environ.get('ADMIN_SMS_API_KEY') 
            
            # رسالة مخصصة للإدارة
            message = f"Mahjoub Online | Admin Access\n\nرمز دخول الإدارة: {otp_code}"
            
            # مثال لطلب إرسال (قم بضبط الـ URL والـ Params حسب مزود الـ SMS الخاص بك)
            # response = requests.post("URL_SERVICE_SMS", json={"to": clean_phone, "text": message})
            
            # حالياً سنضع منطق الطباعة للتجربة حتى تختار مزود الـ SMS الخاص بك:
            print(f"🔐 [Admin OTP] إرسال للإدارة: {otp_code} إلى الرقم: {clean_phone}")
            
            # سنفترض النجاح دائماً في هذه المرحلة حتى تقوم بربط مزود الـ SMS
            return True 
            
        except Exception as e:
            print(f"❌ [Admin Auth Error] {e}")
            return False

# 📂 ملاحظة: لربط هذا الملف بـ otp_db.py، أنشئ ملف dispatcher في مجلد auth_portal 
# ليكون هو الجسر الذي يستدعي هذه الدالة.
