# coding: utf-8
# 📂 apps/vendors/routes.py

from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_user, login_required, logout_user
from apps import db
from apps.vendors.vendor_auth_service import VendorAuthService
from apps.models.otp_db import OTPVerification
from apps.models.supplier_db import Supplier
from apps.models.marketer_db import Marketer

vendors_bp = Blueprint('vendors', __name__, template_folder='templates')

@vendors_bp.route('/')
def index():
    return redirect(url_for('vendors.login'))

@vendors_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('vendor/login.html')

    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "بيانات غير صالحة"}), 400

        login_type = data.get('type')
        # تنظيف رقم الهاتف لضمان التوافق ومنع التكرار الناتجة عن المسافات
        phone = data.get('phone', '').replace(" ", "").replace("-", "")
        otp = data.get('otp')
        username = data.get('username')
        password = data.get('password')

        # --- 1. دخول المسوقين (نظام تقليدي) ---
        if login_type == 'marketer':
            user = Marketer.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                return jsonify({"status": "success", "redirect": "/marketers/dashboard"})
            return jsonify({"status": "error", "message": "بيانات الدخول غير صحيحة"}), 401

        # --- 2. دخول الموردين (نظام سيادي عبر OTP) ---
        
        # أ) طلب إرسال رمز التحقق
        if phone and not otp:
            new_otp = OTPVerification.generate_otp(phone)
            if new_otp and VendorAuthService.initiate_login(phone, new_otp):
                return jsonify({"status": "success", "message": "تم إرسال رمز التحقق عبر واتساب"})
            return jsonify({"status": "error", "message": "فشل إرسال الرمز، يرجى المحاولة لاحقاً"}), 500

        # ب) التحقق من الرمز
        if phone and otp:
            if OTPVerification.verify_otp(phone, otp):
                # البحث عن المورد في قاعدة البيانات
                supplier = Supplier.query.filter_by(_owner_phone=phone).first()
                
                # إذا لم يكن مسجلاً، ننشئ سجل جديد له (مرة واحدة فقط)
                if not supplier:
                    supplier = Supplier(_owner_phone=phone)
                    db.session.add(supplier)
                    db.session.commit()
                
                # تسجيل دخول المورد (سواء كان قديماً أو جديداً)
                login_user(supplier)
                
                # توجيه المورد (إذا أكمل بياناته يذهب للوحة التحكم، وإلا يذهب للإعداد)
                is_ready = getattr(supplier, 'is_setup_complete', False)
                redirect_url = "/supplier/dashboard" if is_ready else "/vendors/setup"
                
                return jsonify({
                    "status": "success", 
                    "message": "تم التحقق بنجاح، جاري تحويلك...", 
                    "redirect": redirect_url
                })
            
            return jsonify({"status": "error", "message": "رمز التحقق خاطئ أو منتهي الصلاحية"}), 400

        return jsonify({"status": "error", "message": "بيانات غير مكتملة"}), 400

    except Exception as e:
        db.session.rollback()
        print(f"CRITICAL ERROR in login: {str(e)}")
        return jsonify({"status": "error", "message": "خطأ داخلي في النظام"}), 500

@vendors_bp.route('/dashboard')
@login_required
def dashboard():
    return redirect(url_for('supplier_dashboard.dashboard'))

@vendors_bp.route('/setup', methods=['GET', 'POST'])
@login_required
def setup_profile():
    return render_template('vendor/setup.html')

@vendors_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('vendors.login'))
