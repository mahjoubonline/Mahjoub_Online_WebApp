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
        # استخدام get_json() لضمان استقبال البيانات بشكل آمن
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
                print(f"DEBUG: Failed to initiate login for {phone}")
                return jsonify({"status": "error", "message": "فشل إرسال الرمز، تحقق من الرقم أو الخدمة"}), 500

        # مرحلة 2: التحقق من الرمز (Verification Request)
        if phone and otp:
            if OTPVerification.verify_otp(phone, otp):
                # التحقق من وجود المورد في قاعدة البيانات
                supplier = Supplier.query.filter_by(_owner_phone=phone).first() 
                
                # إذا كان موجوداً نسجل دخوله
                if supplier:
                    login_user(supplier)
                    return jsonify({"status": "success", "redirect": "/vendors/dashboard"})
                
                # إذا كان مستخدماً جديداً، توجيهه لصفحة التسجيل أو إكمال البيانات
                return jsonify({"status": "success", "redirect": "/vendors/setup"})
            
            return jsonify({"status": "error", "message": "رمز التحقق غير صحيح أو منتهي"}), 400
            
        return jsonify({"status": "error", "message": "بيانات غير مكتملة"}), 400

    except Exception as e:
        # هذا السطر سيكشف الخطأ الحقيقي في Logs ريندر
        print(f"CRITICAL SYSTEM ERROR in /login: {str(e)}")
        return jsonify({"status": "error", "message": f"خطأ داخلي: {str(e)}"}), 500

@vendors_bp.route('/quick-login', methods=['POST'])
def quick_login():
    """دخول سريع للمطورين أو للعمليات الخاصة"""
    return jsonify({"status": "success", "redirect": "/vendors/dashboard"})

@vendors_bp.route('/dashboard')
@login_required
def dashboard():
    return "مرحباً بك في لوحة تحكم المورد"

@vendors_bp.route('/setup', methods=['GET', 'POST'])
@login_required
def setup_profile():
    # هنا سيقوم المورد بتعبئة بياناته في supplier_profile_db.py
    return "صفحة إكمال بيانات المورد"
