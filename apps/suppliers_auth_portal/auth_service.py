# coding: utf-8
# 📂 apps/suppliers_auth_portal/auth_service.py - خدمة إرسال التحقق للموردين وسوبلر عبر HyperSend

import os
import re
import requests

class VendorAuthService:
    @staticmethod
    def initiate_login(phone, otp_code):
        """
        إرسال رمز التحقق الـ OTP الخاص بالموردين والمسوقين عبر خدمة HyperSend (WhatsApp API).
        """
        # 1. جلب بيانات التوثيق من متغيرات بيئة ريندر (Render)
        api_key = os.environ.get('HYPERSEND_API_KEY', '1389|sudxqnVbeF8d1HHi1a8ogGRRzkb6LOJDXILMe0Pg70dbd12c')
        instance_id = os.environ.get('HYPERSEND_INSTANCE_ID', 'a219739b-b1b0-4c0b-858c-45d4d309e27f')

        # 2. تنظيف الرقم وتجهيز الصياغة الدولية (بدون علامة + لـ HyperSend)
        clean_phone = re.sub(r'[^\d]', '', str(phone))
        if clean_phone.startswith('00967'):
            clean_phone = clean_phone[2:]
        elif clean_phone.startswith('7') and len(clean_phone) == 9:
            clean_phone = '967' + clean_phone
        elif clean_phone.startswith('07') and len(clean_phone) == 10:
            clean_phone = '967' + clean_phone[1:]

        # 3. صياغة رسالة محجوب أونلاين السيادية
        message_body = (
            f"*Mahjoub Online | الشركاء والموردين*\n\n"
            f"رمز التحقق الأمني الخاص بك هو: *{otp_code}*\n\n"
            f"يرجى عدم مشاركة هذا الرمز مع أي شخص.\n"
            f"— محجوب أونلاين | سوقك الذكي"
        )

        # 4. تجهيز الطلب لـ HyperSend API
        # الرابط المعتمد لإرسال الرسائل النصية عبر الواتساب في HyperSend
        url = "https://hypersend.net/api/v1/messages/send-text"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "instance_id": instance_id,
            "to": clean_phone,
            "message": message_body
        }

        try:
            # 5. إطلاق طلب الإرسال الفعلي
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            res_data = response.json()

            if response.status_code == 200 and (res_data.get('status') == 'success' or res_data.get('success') is True):
                print(f"✅ [Vendor OTP Sent via HyperSend] تم الإرسال بنجاح للرقم: {clean_phone}")
                return True
            else:
                print(f"❌ [HyperSend API Error] الرد: {response.text}")
                return False

        except Exception as e:
            print(f"🚨 CRITICAL [Vendor HyperSend Error]: {str(e)}")
            return False
