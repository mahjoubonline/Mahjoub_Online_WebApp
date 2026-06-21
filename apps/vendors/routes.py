# coding: utf-8
# 📂 apps/vendors/routes.py

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_user, login_required, logout_user
from apps.vendors.vendor_auth_service import VendorAuthService
from apps.models.otp_db import OTPVerification
from apps.models.supplier_db import Supplier
from apps.models.marketer_db import Marketer

# تعريف الـ Blueprint الخاص بنظام الموردين والمسوقين
vendors_bp = Blueprint('vendors', __name__, template_folder='templates')

@vendors_bp.route('/login', methods=['GET', 'POST'])
def login():
    """مسار موحد لإدارة تسجيل دخول الموردين (OTP) والمسوقين (كلمة مرور)"""
    
    # عند طلب الصفحة: عرض الواجهة
    if request.method == 'GET':
        return render_template('vendor/login.html')

    # عند إرسال البيانات (JSON API)
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "بيانات غير صالحة"}), 400

        login_type = data.get('type') # 'vendor' أو 'marketer'
        phone = data.get('phone')
        otp = data.get('otp')
        username = data.get('username')
        password = data.get('password')

        # --- المرحلة أ: دخول المسوقين (اعتماد تقليدي) ---
        if login_type == 'marketer':
            user = Marketer.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                return jsonify({"status": "success", "redirect": "/marketers/dashboard"})
            return jsonify({"status": "error", "message": "بيانات الدخول غير صحيحة"}), 401

        # --- المرحلة ب: دخول الموردين (تشفير سيادي عبر OTP) ---
        
        # 1. طلب إرسال رمز التحقق
        if phone and not otp:
            new_otp = OTPVerification.generate_otp(phone)
            if new_otp and VendorAuthService.initiate_login(phone, new_otp):
                return jsonify({"status": "success", "message": "تم إرسال رمز التشفير إلى واتساب الخاص بك"})
            return jsonify({"status": "error", "message": "فشل إرسال الرمز، يرجى مراجعة الخدمة"}), 500

        # 2. التحقق من رمز الدخول
        if phone and otp:
            if OTPVerification.verify_otp(phone, otp):
                supplier = Supplier.query.filter_by(_owner_phone=phone).first()
                
                # إذا كان مورداً موجوداً: دخول
                if supplier:
                    login_user(supplier)
                    return jsonify({"status": "success", "redirect": "/vendors/dashboard"})
                
                # إذا كان مورداً جديداً: توجيه لإكمال البيانات
                return jsonify({"status": "success", "redirect": "/vendors/setup"})
            
            return jsonify({"status": "error", "message": "رمز التحقق خاطئ أو منتهي الصلاحية"}), 400

        return jsonify({"status": "error", "message": "بيانات غير مكتملة"}), 400

    except Exception as e:
        print(f"CRITICAL SYSTEM ERROR: {str(e)}")
        return jsonify({"status": "error", "message": "خطأ داخلي في النظام، يرجى التواصل مع الدعم"}), 500

# --- لوحة التحكم والعمليات ---

@vendors_bp.route('/dashboard')
@login_required
def dashboard():
    return "مرحباً بك في لوحة تحكم الشركاء السيادية"

@vendors_bp.route('/setup', methods=['GET', 'POST'])
@login_required
def setup_profile():
    return "صفحة إكمال بيانات المورد - قيد التطوير"

@vendors_bp.route('/logout')
def logout():
    logout_user()
    return jsonify({"status": "success", "message": "تم تسجيل الخروج"})
