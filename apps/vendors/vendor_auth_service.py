# coding: utf-8
# 📂 apps/vendors/vendor_auth_service.py - طبقة المصادقة والاتصال الآمن

from functools import wraps
from flask import session, redirect, url_for
from apps.models.otp_db import OTPVerification
from apps.extensions import db
import requests # مكتبة مطلوبة لإرسال طلبات الـ API

def vendor_login_required(f):
    """حارس المسارات: التأكد من تسجيل الدخول باستخدام الجلسة الآمنة"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('vendor_authenticated'):
            return redirect(url_for('vendors.login_page'))
        return f(*args, **kwargs)
    return decorated_function

def send_whatsapp_otp(phone, otp):
    """
    وظيفة إرسال الرمز عبر الواتساب.
    يجب استبدال البيانات أدناه ببيانات الـ API الخاص بك بعد الحصول على القالب المعتمد من ميتا.
    """
    # مثال توضيحي للربط مع WhatsApp Cloud API
    api_url = "https://graph.facebook.com/v18.0/YOUR_PHONE_NUMBER_ID/messages"
    headers = {
        "Authorization": "Bearer YOUR_ACCESS_TOKEN",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "template",
        "template": {
            "name": "otp_verification_template", # اسم القالب المعتمد
            "language": {"code": "ar"},
            "components": [{"type": "body", "parameters": [{"type": "text", "text": otp}]}]
        }
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        return response.status_code == 200
    except Exception as e:
        print(f"Error in WhatsApp API: {e}")
        return False

def generate_and_send_otp(email, phone):
    """توليد رمز عبر قاعدة البيانات وإرساله عبر الواتساب"""
    # 1. توليد الرمز عبر النموذج الآمن
    raw_otp = OTPVerification.generate_otp(email)
    
    # 2. إرسال الرمز عبر الواتساب
    success = send_whatsapp_otp(phone, raw_otp)
    
    if success:
        print(f"DEBUG: تم إرسال الرمز {raw_otp} بنجاح إلى الواتساب {phone}")
    else:
        print(f"DEBUG: فشل إرسال الرمز إلى {phone}")
        
    return success

def verify_otp_logic(email, user_input):
    """التحقق باستخدام النموذج السيادي في قاعدة البيانات"""
    return OTPVerification.verify_otp(email, user_input)
