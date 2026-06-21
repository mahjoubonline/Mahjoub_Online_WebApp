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
        # استقبال البيانات من المتصفح
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "لم يتم استلام بيانات"}), 400

        phone = data.get('phone')
        otp = data.get('otp')

        # مرحلة 1: طلب الرمز (إرسال OTP)
        if phone and not otp:
            if VendorAuthService.initiate_login(phone):
                return jsonify({"status": "success", "message": "تم إرسال الرمز إلى واتساب"})
            else:
                # تسجيل الخطأ في الـ Logs لتتبع المشكلة دون إيقاف النظام
                print(f"DEBUG: Service busy or disconnected for {phone}")
                return jsonify({
                    "status": "warning", 
                    "message": "خدمة الرسائل غير متاحة حالياً، يرجى المحاولة بعد قليل أو التأكد من حالة اتصال واتساب."
                }), 200

        # مرحلة 2: التحقق من الرمز (إتمام الدخول)
        if phone and otp:
            # التحقق من صحة الرمز من قاعدة البيانات
            if OTPVerification.verify_otp(phone, otp):
                supplier = Supplier.query.filter_by(_owner_phone=phone).first() 
                
                # إذا كان المورد مسجلاً مسبقاً
                if supplier:
                    login_user(supplier)
                    return jsonify({"status": "success", "redirect": "/vendors/dashboard"})
                
                # إذا كان مورداً جديداً (يتم توجيهه لإكمال بياناته)
                return jsonify({"status": "success", "redirect": "/vendors/setup"})
            
            return jsonify({"status": "error", "message": "رمز التحقق غير صحيح أو منتهي"}), 400
            
        return jsonify({"status": "error", "message": "بيانات غير مكتملة"}), 400

    except Exception as e:
        # تسجيل الأخطاء الحرجة في سجلات ريندر
        print(f"CRITICAL SYSTEM ERROR in /login: {str(e)}")
        return jsonify({"status": "error", "message": "حدث خطأ غير متوقع في النظام"}), 500

@vendors_bp.route('/quick-login', methods=['POST'])
def quick_login():
    """دخول سريع للمطورين (لأغراض التطوير)"""
    return jsonify({"status": "success", "redirect": "/vendors/dashboard"})

@vendors_bp.route('/dashboard')
@login_required
def dashboard():
    return "مرحباً بك في لوحة تحكم المورد"

@vendors_bp.route('/setup', methods=['GET', 'POST'])
@login_required
def setup_profile():
    return "صفحة إكمال بيانات المورد"
