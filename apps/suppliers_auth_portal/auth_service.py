# coding: utf-8
# 📂 apps/suppliers_auth_portal/auth_service.py - نظام إرسال رموز الموردين (HyperSender V2 المحصن)

import os
import requests
import time

class VendorAuthService:
    @staticmethod
    def initiate_login(phone, otp_code=None, retries=3):
        """
        إرسال طلب التحقق للموردين عبر API HyperSender V2.
        ملاحظة: هذا النظام يعتمد على الـ OTP Generator الخاص بـ HyperSender مباشرة.
        """
        # جلب المفتاح مع حذف أي مسافات زائدة قد تؤدي لخطأ 401
        api_key = os.environ.get('HYPERSEND_API_KEY', '572|GiAmlkPjuWPLAYThjSTenfaSruio6azmJ0laq0p1b30dd5a').strip()
        
        # تنظيف الرقم والتأكد من صيغة 967xxxxxxxxx@c.us
        clean_phone = "".join(filter(str.isdigit, str(phone)))
        if not clean_phone.startswith('967'):
            clean_phone = '967' + clean_phone.lstrip('0')
        
        formatted_chat_id = f"{clean_phone}@c.us"

        # الرابط المعتمد لخدمة OTP V2
        url = "https://app.hypersender.com/api/otp/v2/request-code"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # الهيكل المعتمد في V2
        payload = {
            "chatId": formatted_chat_id,
            "length": 6,
            "useLetter": False,
            "useNumber": True,
            "allCapital": False,
            "name": "MahjoubOnline",
            "expires": 1800
        }

        print(f"DEBUG: محاولة إرسال OTP للمورد {formatted_chat_id} إلى الرابط {url}")

        for attempt in range(retries):
            try:
                response = requests.post(url, json=payload, headers=headers, timeout=20)
                
                # طباعة تفاصيل الاستجابة للتشخيص
                print(f"DEBUG: المحاولة {attempt+1} - الحالة: {response.status_code}")
                
                if response.status_code == 200:
                    res_data = response.json()
                    # التحقق من أن الاستجابة تحتوي على مؤشر نجاح
                    if res_data.get('status') == 'success' or 'id' in res_data:
                        print(f"✅ [Vendor OTP Sent V2] تم إرسال الرمز بنجاح.")
                        return True
                    else:
                        print(f"⚠️ [HyperSender Warning] الرد لم يحتوي على status success: {res_data}")
                else:
                    print(f"❌ [HyperSender V2 Error] المحاولة {attempt+1} - النص: {response.text}")
                
            except Exception as e:
                print(f"🚨 [Vendor V2 Connection Error] محاولة {attempt + 1}: {str(e)}")
            
            time.sleep(2) # انتظار قبل المحاولة التالية

        return False
