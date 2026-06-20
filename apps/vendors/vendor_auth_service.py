# coding: utf-8
# 📂 apps/vendors/vendor_auth_service.py

import requests
import logging
from flask import session, redirect, url_for
from functools import wraps
from apps.models.otp_db import OTPVerification

# إعداد الـ Logger لمراقبة العمليات في Render
logger = logging.getLogger("mahjoub_auth")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO)

def send_whatsapp_otp(phone, otp_code):
    """إرسال الرمز عبر خدمة TextMeBot مع تنظيف الرقم من الرموز الزائدة"""
    clean_phone = "".join(filter(str.isdigit, str(phone)))
    api_key = "rb3tZFnHRcsN" 
    message = f"رمز التحقق الخاص بك في محجوب أونلاين هو: {otp_code}"
    url = "http://api.textmebot.com/send.php"
    
    params = {"recipient": clean_phone, "apikey": api_key, "text": message}
    
    try:
        logger.info(f"محاولة إرسال واتساب لـ: {clean_phone}")
        response = requests.get(url, params=params, timeout=10)
        logger.info(f"رد TextMeBot: {response.status_code} - {response.text}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"خطأ في الاتصال بـ TextMeBot: {str(e)}")
        return False

def trigger_otp_process(email, full_phone):
    """توليد الرمز وإرساله عبر الواتساب"""
    logger.info(f"بدء عملية الـ OTP لـ: {email}")
    try:
        otp = OTPVerification.generate_otp(email, expires_in_minutes=5)
        logger.info(f"تم توليد الرمز بنجاح لـ {email}")
        
        success = send_whatsapp_otp(full_phone, otp)
        logger.info(f"نتيجة إرسال الواتساب: {success}")
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
