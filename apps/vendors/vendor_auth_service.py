# coding: utf-8
# 📂 apps/vendors/vendor_auth_service.py

import requests
from functools import wraps
from flask import session, redirect, url_for, current_app
from apps.models.otp_db import OTPVerification

def vendor_login_required(f):
    """ديكوريتور (Decorator) لحماية المسارات التي تتطلب تسجيل دخول المورد"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'vendor_authenticated' not in session:
            return redirect(url_for('vendors.login_page'))
        return f(*args, **kwargs)
    return decorated_function

def trigger_otp_process(email, phone):
    """
    دالة مركزية لإنشاء رمز التحقق وإرساله عبر واتساب.
    تستخدم نموذج OTPVerification لتخزين الرمز مشفراً.
    """
    # 1. إنشاء رمز مشفر وتخزينه في قاعدة البيانات
    otp_code = OTPVerification.generate_otp(email)
    
    # 2. إرسال الرمز عبر الواتساب
    return send_whatsapp_otp(phone, otp_code)

def send_whatsapp_otp(phone, otp):
    """إرسال الرمز عبر الواتساب باستخدام الإعدادات المركزية"""
    
    phone_number_id = current_app.config.get('WHATSAPP_PHONE_NUMBER_ID')
    access_token = current_app.config.get('WHATSAPP_ACCESS_TOKEN')
    
    if not access_token or not phone_number_id:
        print("خطأ: إعدادات WhatsApp غير مكتملة في البيئة")
        return False

    api_url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "template",
        "template": {
            "name": "otp_verification_template", 
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

def verify_vendor_otp(email, input_otp):
    """
    التحقق من رمز المستخدم باستخدام منطق السيادة الأمنية في النموذج
    """
    return OTPVerification.verify_otp(email, input_otp)
