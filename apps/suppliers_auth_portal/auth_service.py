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
        معالجة كاملة للأخطاء لضمان استقرار السيرفر.
        """
        # جلب المفتاح مع حذف أي مسافات زائدة
        api_key = os.environ.get('HYPERSEND_API_KEY', '572|GiAmlkPjuWPLAYThjSTenfaSruio6azmJ0laq0p1b30dd5a').strip()
        
        # تنظيف الرقم
        clean_phone = "".join(filter(str.isdigit, str(phone)))
        if not clean_phone.startswith('967'):
            clean_phone = '967' + clean_phone.lstrip('0')
        
        formatted_chat_id = f"{clean_phone}@c.us"
        url = "https://app.hypersender.com/api/otp/v2/request-code"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "chatId": formatted_chat_id,
            "length": 6,
            "useLetter": False,
            "useNumber": True,
            "allCapital": False,
            "name": "MahjoubOnline",
            "expires": 1800
        }

        for attempt in range(retries):
            try:
                # استخدام timeout صارم لضمان عدم تعليق السيرفر
                response = requests.post(url, json=payload, headers=headers, timeout=10)
                
                # التحقق من نجاح الطلب برمجياً
                if response.status_code == 200:
                    res_data = response.json()
                    if res_data.get('status') == 'success' or 'id' in res_data:
                        return True
                    else:
                        print(f"⚠️ [HyperSender] استجابة غير متوقعة: {res_data}")
                else:
                    print(f"❌ [HyperSender] فشل الاتصال برمز: {response.status_code}")
                
            except requests.exceptions.RequestException as e:
                # خطأ في الاتصال (Network, Timeout, etc) - السيرفر لا ينهار هنا
                print(f"🚨 [Vendor Connection Error] محاولة {attempt + 1}: {str(e)}")
            except Exception as e:
                # أي خطأ برمجي آخر - السيرفر يبقى يعمل
                print(f"💥 [Critical Logic Error] {str(e)}")
            
            # انتظار قصير بين المحاولات
            time.sleep(2)

        return False
