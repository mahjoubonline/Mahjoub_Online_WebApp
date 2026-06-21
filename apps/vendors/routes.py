# coding: utf-8
# 📂 apps/vendors/routes.py

from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_user, login_required, logout_user
from apps import db
from apps.vendors.vendor_auth_service import VendorAuthService
from apps.models.otp_db import OTPVerification
from apps.models.supplier_db import Supplier
from apps.models.marketer_db import Marketer
import uuid 

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
        raw_phone = data.get('phone', '')
        phone = "".join(filter(str.isdigit, raw_phone))
        otp = data.get('otp')
        username = data.get('username')
        password = data.get('password')

        # --- 1. دخول المسوقين ---
        if login_type == 'marketer':
            user = Marketer.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                return jsonify({"status": "success", "redirect": "/marketers/dashboard"})
            return jsonify({"status": "error", "message": "بيانات الدخول غير صحيحة"}), 401

        # --- 2. دخول الموردين (نظام صامت) ---
        # أ) إرسال رمز التحقق
        if phone and not otp:
            new_otp = OTPVerification.generate_otp(phone)
            if new_otp and VendorAuthService.initiate_login(phone, new_otp):
                return jsonify({"status": "success", "message": "تم إرسال رمز التحقق"})
            return jsonify({"status": "error", "message": "فشل إرسال الرمز"}), 500

        # ب) التحقق من الرمز وتسجيل الدخول
        if phone and otp:
            if OTPVerification.verify_otp(phone, otp):
                supplier = Supplier.query.filter_by(_owner_phone=phone).first()
                
                # إذا لم يكن موجوداً، ننشئه (بدون إخبار المستخدم بأي شيء)
                if not supplier:
                    supplier = Supplier(
                        _owner_phone=phone,
                        username=f"vendor_{uuid.uuid4().hex[:8]}",
                        password_hash="temp_pass",
                        trade_name="جديد"
                    )
                    db.session.add(supplier)
                    db.session.commit()
                
                # تسجيل الدخول دائماً (سواء كان قديماً أو جديداً)
                login_user(supplier)
                
                # توجيه ذكي: للوحة التحكم إذا أكمل بياناته، أو لصفحة الإعداد إذا كان "جديداً"
                is_ready = getattr(supplier, 'is_setup_complete', False)
                return jsonify({
                    "status": "success", 
                    "redirect": "/supplier/dashboard" if is_ready else "/vendors/setup"
                })
            
            return jsonify({"status": "error", "message": "رمز التحقق خاطئ"}), 400

        return jsonify({"status": "error", "message": "بيانات غير مكتملة"}), 400

    except Exception as e:
        db.session.rollback()
        print(f"CRITICAL ERROR: {str(e)}") 
        return jsonify({"status": "error", "message": "حدث خطأ أثناء الاتصال بقاعدة البيانات"}), 500

@vendors_bp.route('/dashboard')
@login_required
def dashboard():
    # التحويل للـ Blueprint الخاص بلوحة التحكم
    return redirect(url_for('vendor_dashboard.dashboard'))

@vendors_bp.route('/setup', methods=['GET', 'POST'])
@login_required
def setup_profile():
    return render_template('vendor/setup.html')

@vendors_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('vendors.login'))
