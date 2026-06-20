from functools import wraps
from flask import session, redirect, url_for
from apps.models.otp_db import OTPVerification
from apps.extensions import db

def vendor_login_required(f):
    """حارس المسارات: التأكد من تسجيل الدخول باستخدام الجلسة الآمنة"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('vendor_authenticated'):
            return redirect(url_for('vendors.login_page'))
        return f(*args, **kwargs)
    return decorated_function

def generate_and_send_otp(email, phone):
    """توليد رمز عبر قاعدة البيانات (استبدال الجلسات بالنموذج الآمن)"""
    # استخدام الدالة الجاهزة في otp_db.py
    raw_otp = OTPVerification.generate_otp(email)
    
    # هنا سيتم ربط مزود الخدمة الفعلي (SMS/Email)
    print(f"DEBUG: تم إرسال الرمز {raw_otp} إلى البريد {email}")
    return True

def verify_otp_logic(email, user_input):
    """التحقق باستخدام النموذج السيادي في قاعدة البيانات"""
    # استخدام الدالة الجاهزة في otp_db.py
    return OTPVerification.verify_otp(email, user_input)
