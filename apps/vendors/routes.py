# 📂 apps/vendors/routes.py

from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for
from .vendor_auth_service import vendor_login_required, generate_and_send_otp, verify_otp_logic

# تعريف الـ Blueprint للموردين
vendors_bp = Blueprint('vendors', __name__, template_folder='templates')

@vendors_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    """صفحة تسجيل الدخول التي تستقبل بيانات المورد وتدير عملية الـ OTP"""
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        phone = data.get('phone')
        otp = data.get('otp')

        # حالة 1: طلب إرسال رمز التحقق
        if email and phone and not otp:
            generate_and_send_otp(email, phone)
            return jsonify({"status": "pending", "message": "تم إرسال رمز التأكيد إلى بياناتك"})

        # حالة 2: التحقق من رمز الـ OTP المدخل
        if otp:
            if verify_otp_logic(otp):
                session['vendor_authenticated'] = True
                session['vendor_email'] = email
                session['vendor_name'] = "المورد الكريم"
                return jsonify({"status": "success", "message": "تم التحقق بنجاح", "redirect": url_for('vendors.dashboard')})
            else:
                return jsonify({"status": "error", "message": "رمز التأكيد غير صحيح"}), 400
        
        return jsonify({"status": "error", "message": "بيانات غير مكتملة"}), 400
    
    return render_template('vendor/login.html')

@vendors_bp.route('/quick-login', methods=['POST'])
def quick_login():
    """دخول سريع عابر للأنظمة"""
    session['vendor_authenticated'] = True
    session['vendor_name'] = "مورد (دخول سريع)"
    return jsonify({"status": "success", "redirect": url_for('vendors.dashboard')})

@vendors_bp.route('/dashboard')
@vendor_login_required  # حارس المسارات
def dashboard():
    """لوحة تحكم المورد (محمية)"""
    return render_template('vendor/dashboard.html', vendor_name=session.get('vendor_name'))

@vendors_bp.route('/logout')
def logout():
    """تسجيل الخروج وإنهاء الجلسة"""
    session.clear()
    return redirect(url_for('vendors.login_page'))
