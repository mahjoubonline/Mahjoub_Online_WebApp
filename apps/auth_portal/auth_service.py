# coding: utf-8
# 📂 apps/auth_portal/auth_service.py - خدمة إرسال التحقق للإدارة العليا عبر HyperSend (نسخة Anti-Reset المحصنة)

import os
import re
import requests

class AdminAuthService:
    @staticmethod
    def initiate_login(phone, otp_code):
        """
        إرسال رمز التحقق الـ OTP الخاص بالإدارة العليا عبر خدمة HyperSend المستقرة مع حماية ضد قفل الاتصال فجأة.
        """
        api_key = os.environ.get('HYPERSEND_API_KEY', '1389|sudxqnVbeF8d1HHi1a8ogGRRzkb6LOJDXILMe0Pg70dbd12c')
        instance_id = os.environ.get('HYPERSEND_INSTANCE_ID', 'a219739b-b1b0-4c0b-858c-45d4d309e27f')

        clean_phone = re.sub(r'[^\d]', '', str(phone))
        if clean_phone.startswith('00967'):
            clean_phone = clean_phone[2:]
        elif clean_phone.startswith('7') and len(clean_phone) == 9:
            clean_phone = '967' + clean_phone
        elif clean_phone.startswith('07') and len(clean_phone) == 10:
            clean_phone = '967' + clean_phone[1:]

        message_body = (
            f"*Mahjoub Online | Admin Access*\n\n"
            f"رمز دخول الإدارة الخاص بك هو: *{otp_code}*\n\n"
            f"— محجوب أونلاين | النظام الأمني"
        )

        # محاولة الإرسال باستخدام الرابط الرئيسي مع تمرير المفتاح كـ Query Parameter لحل مشكلة الـ Reset
        url = f"https://hypersend.net/api/v1/messages/send-text?api_key={api_key}"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        payload = {
            "instance_id": instance_id,
            "to": clean_phone,
            "message": message_body
        }

        try:
            # استخدام Session لإبقاء الاتصال مستقراً وآمناً
            with requests.Session() as session:
                session.headers.update(headers)
                response = session.post(url, json=payload, timeout=20)
                
            res_data = response.json()

            if response.status_code == 200 and (res_data.get('status') == 'success' or res_data.get('success') is True):
                print(f"✅ [Admin OTP Sent via HyperSend] تم إرسال رمز المسؤول بنجاح!")
                return True
            else:
                print(f"❌ [Admin HyperSend API Response Error] الحالة: {response.status_code} - الرد: {response.text}")
                return False
                
        except Exception as e:
            print(f"🚨 CRITICAL [Admin HyperSend Error]: {str(e)}")
            return False
