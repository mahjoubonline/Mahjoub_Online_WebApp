# coding: utf-8
# 📂 apps/auth_portal/auth_service.py - خدمة إرسال التحقق للإدارة العليا عبر Twilio (الإصدار المحمي)

import os
import re
from twilio.rest import Client

class AdminAuthService:
    @staticmethod
    def initiate_login(phone, otp_code):
        """
        إرسال رمز التحقق الـ OTP الخاص بالإدارة العليا عبر خدمة Twilio الرسمية المستقرة.
        """
        # 1. جلب بيانات التوثيق الصارمة من متغيرات بيئة ريندر (Render)
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        twilio_number = os.environ.get('TWILIO_NUMBER')

        # تحقق استباقي لمنع محاولات الإرسال الفاشلة إذا كانت المتغيرات ناقصة
        if not all([account_sid, auth_token, twilio_number]):
            print("🚨 [Admin Twilio Config Error] بيانات التوثيق للإدارة غير مكتملة في Render!")
            return False

        # 2. تنظيف رقم الهاتف وتجهيز الصياغة الدولية المعتمدة لـ Twilio
        clean_phone = re.sub(r'[^\d]', '', str(phone))
        
        if clean_phone.startswith('00967'):
            clean_phone = clean_phone[2:]
        elif clean_phone.startswith('7') and len(clean_phone) == 9:
            clean_phone = '967' + clean_phone
        elif clean_phone.startswith('07') and len(clean_phone) == 10:
            clean_phone = '967' + clean_phone[1:]
        
        # إضافة علامة الزائد (+) الإلزامية لبروتوكول Twilio
        destination_phone = f"+{clean_phone}"

        # 3. صياغة الرسالة الرسمية الحصرية الخاصة بالإدارة العليا
        message_body = (
            f"Mahjoub Online | Admin Access\n\n"
            f"رمز دخول الإدارة الخاص بك هو: {otp_code}\n\n"
            f"— محجوب أونلاين | النظام الأمني"
        )

        try:
            # 4. بناء الجلسة البرمجية مع سيرفرات Twilio
            client = Client(account_sid, auth_token)

            # 5. التمييز الذكي لنوع قناة الإرسال (WhatsApp أو SMS عادية) بناءً على الرقم المدخل
            if twilio_number.startswith('whatsapp:') or "whatsapp" in twilio_number.lower():
                from_number = twilio_number if twilio_number.startswith('whatsapp:') else f"whatsapp:{twilio_number}"
                to_number = f"whatsapp:{destination_phone}"
            else:
                from_number = twilio_number
                to_number = destination_phone

            # 6. إطلاق طلب الإرسال الفعلي
            message = client.messages.create(
                body=message_body,
                from_=from_number,
                to=to_number
            )

            print(f"✅ [Admin OTP Sent via Twilio] تم إرسال رمز الإدارة بنجاح! معرف الرسالة: {message.sid}")
            return True
            
        except Exception as e:
            print(f"🚨 CRITICAL [Admin Auth Twilio Error]: {str(e)}")
            return False
