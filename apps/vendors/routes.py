# coding: utf-8
# 📂 apps/vendors/routes.py

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_user, login_required
from apps.vendors.vendor_auth_service import VendorAuthService
from apps.models.otp_db import OTPVerification
from apps.models.supplier_db import Supplier

vendors_bp = Blueprint('vendors', __name__, template_folder='templates')

@vendors_bp.route('/login', methods=['GET', 'POST'])
def login():
    """مسار إدارة تسجيل دخول الموردين بأسلوب أمني سيادي"""
    if request.method == 'GET':
        return render_template('vendor/login.html')

    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "بيانات غير صالحة"}), 400

        phone = data.get('phone')
        otp = data.get('otp')

        # --- المرحلة 1: طلب إرسال رمز التحقق ---
        if phone and not otp:
            # توليد الرمز في قاعدة البيانات
            new_otp = OTPVerification.generate_otp(phone)
            
            if new_otp:
                # محاولة الإرسال عبر خدمة واتساب الخارجية
                if VendorAuthService.initiate_login(phone, new_otp):
                    return jsonify({"status": "success", "message": "تم إرسال رمز التشفير إلى واتساب الخاص بك"})
                else:
                    return jsonify({"status": "warning", "message": "خدمة واتساب غير متاحة حالياً، يرجى التأكد من حالة اتصال الرقم"}), 200
            else:
                return jsonify({"status": "error", "message": "فشل إنشاء رمز التحقق في قاعدة البيانات"}), 500

        # --- المرحلة 2: التحقق من رمز الدخول ---
        if phone and otp:
            if OTPVerification.verify_otp(phone, otp):
                supplier = Supplier.query.filter_by(_owner_phone=phone).first()
                
                # إذا كان المورد موجوداً، يتم تسجيل دخوله
                if supplier:
                    login_user(supplier)
                    return jsonify({"status": "success", "redirect": "/vendors/dashboard"})
                
                # إذا كان مورداً جديداً، يتم توجيهه لإعداد ملفه الشخصي
                return jsonify({"status": "success", "redirect": "/vendors/setup"})
            
            return jsonify({"status": "error", "message": "رمز التحقق غير صحيح أو منتهي الصلاحية"}), 400
            
        return jsonify({"status": "error", "message": "بيانات غير مكتملة"}), 400

    except Exception as e:
        # تسجيل الخطأ في الـ Logs الخاصة بالخادم (Render)
        print(f"CRITICAL SYSTEM ERROR in /login: {str(e)}")
        return jsonify({"status": "error", "message": "حدث خطأ غير متوقع، يرجى التواصل مع الدعم الفني"}), 500

@vendors_bp.route('/dashboard')
@login_required
def dashboard():
    return "مرحباً بك في لوحة تحكم المورد السيادية"

@vendors_bp.route('/setup', methods=['GET', 'POST'])
@login_required
def setup_profile():
    return "صفحة إكمال بيانات المورد - قيد التطوير"
