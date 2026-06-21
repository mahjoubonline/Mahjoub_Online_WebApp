# coding: utf-8
# 📂 apps/vendors/routes.py

from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_user, login_required, logout_user
from apps.vendors.vendor_auth_service import VendorAuthService
from apps.models.otp_db import OTPVerification
from apps.models.supplier_db import Supplier
from apps.models.marketer_db import Marketer

# تعريف الـ Blueprint
vendors_bp = Blueprint('vendors', __name__, template_folder='templates')

@vendors_bp.route('/login', methods=['GET', 'POST'])
def login():
    """مسار موحد لإدارة تسجيل دخول الموردين والمسوقين"""
    if request.method == 'GET':
        return render_template('vendor/login.html')

    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "بيانات غير صالحة"}), 400

        login_type = data.get('type') # 'vendor' أو 'marketer'
        phone = data.get('phone')
        otp = data.get('otp')
        username = data.get('username')
        password = data.get('password')

        # --- 1. دخول المسوقين (تقليدي) ---
        if login_type == 'marketer':
            user = Marketer.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                return jsonify({"status": "success", "redirect": "/marketers/dashboard"})
            return jsonify({"status": "error", "message": "اسم المستخدم أو كلمة المرور غير صحيحة"}), 401

        # --- 2. دخول الموردين (سيادي عبر OTP) ---
        
        # أ) طلب إرسال رمز التحقق
        if phone and not otp:
            new_otp = OTPVerification.generate_otp(phone)
            if new_otp and VendorAuthService.initiate_login(phone, new_otp):
                return jsonify({"status": "success", "message": "تم إرسال رمز التشفير إلى واتساب الخاص بك"})
            return jsonify({"status": "error", "message": "فشل إرسال الرمز، تأكد من رقم الهاتف"}), 500

        # ب) التحقق من الرمز
        if phone and otp:
            if OTPVerification.verify_otp(phone, otp):
                supplier = Supplier.query.filter_by(_owner_phone=phone).first()
                
                if supplier:
                    # مورد مسجل مسبقاً
                    login_user(supplier)
                    return jsonify({
                        "status": "success", 
                        "message": "تم التحقق، جاري تحويلك للمنصة اللامركزية", 
                        "redirect": "/supplier/dashboard"
                    })
                
                # مورد جديد (يجب إنشاء سجل مبدئي أولاً)
                # ملاحظة: هنا ننشئ سجل المورد قبل التوجيه لضمان استمرارية الجلسة
                new_supplier = Supplier(_owner_phone=phone) 
                # أضف هنا أي منطق إضافي لإضافة المورد لقاعدة البيانات
                # db.session.add(new_supplier); db.session.commit()
                login_user(new_supplier)
                
                return jsonify({
                    "status": "success", 
                    "message": "تم التفعيل، يرجى إكمال بياناتك", 
                    "redirect": "/vendors/setup"
                })
            
            return jsonify({"status": "error", "message": "رمز التحقق خاطئ أو منتهي الصلاحية"}), 400

        return jsonify({"status": "error", "message": "بيانات غير مكتملة"}), 400

    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")
        return jsonify({"status": "error", "message": "خطأ داخلي في النظام"}), 500

@vendors_bp.route('/dashboard')
@login_required
def dashboard():
    """توجيه المورد للهيكل السيادي الأساسي"""
    return redirect(url_for('supplier_dashboard.dashboard'))

@vendors_bp.route('/setup', methods=['GET', 'POST'])
@login_required
def setup_profile():
    return render_template('vendor/setup.html')

@vendors_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('vendors.login'))
