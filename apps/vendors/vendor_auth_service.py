# 📂 apps/vendors/vendor_auth_service.py

from functools import wraps
from flask import session, redirect, url_for
import random

def vendor_login_required(f):
    """حارس المسارات: التأكد من تسجيل الدخول"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('vendor_authenticated'):
            return redirect(url_for('vendors.login_page'))
        return f(*args, **kwargs)
    return decorated_function

def generate_and_send_otp(email, phone):
    """
    توليد رمز التحقق وتجهيزه للإرسال.
    هنا يتم الربط مع مزود الخدمة (SMS أو Email)
    """
    otp_code = str(random.randint(100000, 999999))
    
    # تخزين الرمز في الجلسة ليتم مقارنته لاحقاً
    session['otp_code'] = otp_code
    session['otp_email'] = email
    
    # مكان ربط الـ API:
    # send_sms(phone, f"رمز التحقق الخاص بك هو: {otp_code}")
    print(f"DEBUG: تم إرسال الرمز {otp_code} إلى {email} / {phone}")
    
    return True

def verify_otp_logic(user_input):
    """
    التحقق من مطابقة الرمز المدخل مع المخزن في الجلسة
    """
    actual_otp = session.get('otp_code')
    if actual_otp and user_input == actual_otp:
        # مسح الرمز بعد استخدامه بنجاح للأمان
        session.pop('otp_code', None)
        return True
    return False
