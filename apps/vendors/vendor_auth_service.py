# coding: utf-8
# 📂 apps/vendors/vendor_auth_service.py

import requests
import logging
from flask import session, redirect, url_for
from functools import wraps
from apps.models.otp_db import OTPVerification

# إعداد الـ Logger
logger = logging.getLogger("mahjoub_auth")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO)

def send_whatsapp_otp(phone, otp_code):
    """إرسال الرمز عبر خدمة TextMeBot المحدثة"""
    # تنظيف الرقم والتأكد أنه يبدأ برمز الدولة بدون +
    clean_phone = "".join(filter(str.isdigit, str(phone)))
    api_key = "rb3tZFnHRcsN" 
    message = f"رمز التحقق الخاص بك في محجوب أونلاين هو: {otp_code}"
    
    # الرابط المحدث بناءً على توثيق TextMeBot الشائع
    url = "https://api.textmebot.com/send"
    
    # تمرير المعاملات كما يتطلبها الـ API بدقة
    params = {
        "phone": clean_phone, 
        "apikey": api_key, 
        "text": message
    }
    
    try:
        logger.info(f"DEBUG: محاولة إرسال واتساب لـ: {clean_phone} عبر الرابط: {url}")
        response = requests.get(url, params=params, timeout=15)
        
        # طباعة الرد كاملاً في الـ Logs للتشخيص
        logger.info(f"DEBUG: TextMeBot Response: {response.status_code} - {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        logger.error(f"خطأ في الاتصال بـ TextMeBot: {str(e)}")
        return False

def trigger_otp_process(email, full_phone):
    """توليد الرمز وإرساله عبر الواتساب"""
    logger.info(f"بدء عملية الـ OTP لـ: {email}")
    try:
        otp = OTPVerification.generate_otp(email, expires_in_minutes=5)
        logger.info(f"تم توليد الرمز {otp} بنجاح لـ {email}")
        
        success = send_whatsapp_otp(full_phone, otp)
        return success
    except Exception as e:
        logger.error(f"خطأ فادح في trigger_otp_process: {str(e)}")
        return False

def verify_vendor_otp(email, otp):
    """التحقق من صحة الرمز"""
    return OTPVerification.verify_otp(email, otp)

def vendor_login_required(f):
    """ديكوريتور لحماية لوحة التحكم"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('vendor_authenticated'):
            return redirect(url_for('vendors.index'))
        return f(*args, **kwargs)
    return decorated_function
