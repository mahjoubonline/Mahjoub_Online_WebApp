# coding: utf-8
# 📂 apps/vendors/routes.py

from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_user, login_required, logout_user
from apps.vendors.vendor_auth_service import VendorAuthService
from apps.models.otp_db import OTPVerification
from apps.models.supplier_db import Supplier

vendors_bp = Blueprint('vendors', __name__, template_folder='templates')

@vendors_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('vendor/login.html')

    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "لم يتم استلام بيانات"}), 400

        phone = data.get('phone')
        otp = data.get('otp')

        # مرحلة 1: طلب الرمز (Login Request)
        if phone and not otp:
            if VendorAuthService.initiate_login(phone):
                return jsonify({"status": "success", "message": "تم إرسال الرمز إلى واتساب"})
            else:
                # هنا التعديل: تحويل فشل الـ API إلى رسالة تنبيه تفاعلية بدلاً من خطأ 500
                print(f"DEBUG: Service busy or disconnected for {phone}")
                return jsonify({
                    "status": "warning", 
                    "message": "خدمة الرسائل غير متاحة حالياً، يرجى المحاولة بعد قليل أو التأكد من حالة اتصال واتساب."
                }), 200

        # مرحلة 2: التحقق من الرمز (Verification Request)
        if phone and otp:
            if OTPVerification.verify_otp(phone, otp):
                supplier = Supplier.query.filter_by(_owner_phone=phone).first() 
                
                if supplier:
                    login_user(supplier)
                    return jsonify({"status": "success", "redirect": "/vendors/dashboard"})
                
                return jsonify({"status": "success", "redirect": "/vendors/setup"})
            
            return jsonify({"status": "error", "message": "رمز التحقق غير صحيح أو منتهي"}), 400
            
        return jsonify({"status": "error", "message": "بيانات غير مكتملة"}), 400

    except Exception as e:
        print(f"CRITICAL SYSTEM ERROR in /login: {str(e)}")
        return jsonify({"status": "error", "message": "حدث خطأ غير متوقع في النظام"}), 500

@vendors_bp.route('/quick-login', methods=['POST'])
def quick_login():
    """دخول سريع للمطورين"""
    return jsonify({"status": "success", "redirect": "/vendors/dashboard"})

@vendors_bp.route('/dashboard')
@login_required
def dashboard():
    return "مرحباً بك في لوحة تحكم المورد"

@vendors_bp.route('/setup', methods=['GET', 'POST'])
@login_required
def setup_profile():
    return "صفحة إكمال بيانات المورد"
