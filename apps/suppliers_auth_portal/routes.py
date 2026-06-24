# coding: utf-8
# 📂 apps/suppliers_auth_portal/routes.py - نظام الدخول للموردين والمسوقين (نسخة HyperSend الكاملة والمستقرة)

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from flask_login import login_user, logout_user, current_user
from apps.extensions import db  
import uuid

# استيراد خدمة الإرسال الخاصة بالموردين المربوطة بـ HyperSend
from apps.suppliers_auth_portal.auth_service import VendorAuthService

# تعريف الـ Blueprint باسم 'suppliers'
suppliers_bp = Blueprint('suppliers', __name__, template_folder='templates')

# جسر إرسال الموردين المستقل (لمنع التداخل مع الإدارة العليا)
class SupplierDispatcher:
    @staticmethod
    def send(phone, code):
        return VendorAuthService.initiate_login(phone, code)

@suppliers_bp.before_request
def check_login():
    """حماية سيادية: فحص الحماية فقط إذا كان الطلب يخص مستخدم غير مسجل وموجه لهذا الـ Blueprint"""
    if request.endpoint in ['suppliers.login', 'suppliers.verify_page', 'static'] or not request.blueprint == 'suppliers':
        return None
    
    if request.endpoint and 'marketers' in request.endpoint:
        return None

    if not current_user.is_authenticated:
        return redirect(url_for('suppliers.login'))

@suppliers_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('suppliers.dashboard'))
        return render_template('suppliers_auth_portal/login.html')

    from apps.models.otp_db import OTPVerification

    try:
        data = request.get_json() if request.is_json else request.form
        if not data:
            return jsonify({"status": "error", "message": "بيانات غير صالحة"}), 400

        login_type = data.get('type')
        
        # --- دخول المسوقين ---
        if login_type == 'marketer':
            username = data.get('username', '').strip()
            password = data.get('password', '')
            
            from apps.models import Marketer
            user = Marketer.query.filter_by(marketing_code=username).first()
            if user and hasattr(user, 'check_password') and user.check_password(password): 
                login_user(user, remember=True)
                return jsonify({"status": "success", "redirect": url_for('marketers.dashboard')})
            return jsonify({"status": "error", "message": "بيانات الدخول غير صحيحة"}), 401

        # --- دخول الموردين (خطوة 1: طلب الرمز) ---
        raw_phone = data.get('phone', '')
        phone = "".join(filter(str.isdigit, raw_phone))

        if not phone:
            return jsonify({"status": "error", "message": "رقم الهاتف مطلوب"}), 400

        # تحويل الرقم للصيغة الدولية المتوافقة مع الإرسال المحلي والدولي
        if len(phone) == 9 and phone.startswith('7'):
            phone = '967' + phone
        elif len(phone) == 10 and phone.startswith('07'):
            phone = '967' + phone[1:]

        # توليد وإرسال الـ OTP الفوري عبر الواتساب باستخدام HyperSend وجسر الإرسال الذكي
        new_otp = OTPVerification.generate_otp(phone, SupplierDispatcher)
        if new_otp:
            return jsonify({"status": "success", "message": "تم إرسال رمز التحقق بنجاح إلى حساب الواتساب الخاص بك"})
        return jsonify({"status": "error", "message": "فشل إرسال الرمز، يرجى المحاولة لاحقاً"}), 500

    except Exception as e:
        db.session.rollback()
        print(f"🚨 [Supplier Auth Error]: {str(e)}")
        return jsonify({"status": "error", "message": "حدث خطأ فني في خادم المصادقة"}), 500


# 🔄 الموجه المشترك لعرض صفحة التحقق والتحقق الفعلي من الـ OTP لمنع تفكك الجلسة
@suppliers_bp.route('/verify', methods=['GET', 'POST'])
def verify_page():
    if current_user.is_authenticated:
        return redirect(url_for('suppliers.dashboard'))
        
    if request.method == 'GET':
        return render_template('suppliers_auth_portal/verify.html')

    # معالجة طلب التحقق الفعلي (POST) المرسل من واجهة verify.html
    from apps.models.otp_db import OTPVerification
    try:
        data = request.get_json() if request.is_json else request.form
        raw_phone = data.get('phone', '')
        phone = "".join(filter(str.isdigit, raw_phone))
        otp = data.get('otp')

        if not phone or not otp:
            return jsonify({"status": "error", "message": "بيانات التحقق غير مكتملة"}), 400

        # تنظيف الرقم وتوحيد الصيغة للفحص داخل قاعدة البيانات
        if len(phone) == 9 and phone.startswith('7'):
            phone = '967' + phone
        elif len(phone) == 10 and phone.startswith('07'):
            phone = '967' + phone[1:]

        if OTPVerification.verify_otp(phone, otp):
            from apps.models import Supplier
            supplier = Supplier.query.filter_by(phone=phone).first()
            
            if not supplier:
                supplier = Supplier(
                    username=f"supplier_{uuid.uuid4().hex[:8]}",
                    supplier_code=f"VEN-{uuid.uuid4().hex[:6].upper()}",
                    phone=phone, 
                    trade_name="مورد جديد لدينا"
                )
                db.session.add(supplier)
                db.session.commit()
            
            # تسجيل الدخول وتثبيت الجلسة بشكل قاطع للمورد
            login_user(supplier, remember=True)
            session.permanent = True
            
            # إرجاع استجابة صريحة بنجاح العملية وتوجيهه للوحة الموردين الرئيسية
            response = jsonify({"status": "success", "redirect": url_for('suppliers.dashboard')})
            return response
        
        return jsonify({"status": "error", "message": "رمز التحقق منتهي أو خاطئ"}), 400

    except Exception as e:
        db.session.rollback()
        print(f"🚨 [Supplier OTP Verify Error]: {str(e)}")
        return jsonify({"status": "error", "message": "حدث خطأ أثناء فحص رمز التحقق"}), 500


@suppliers_bp.route('/dashboard')
def dashboard():
    return "مرحباً بك في لوحة تحكم الموردين لمنصة محجوب أونلاين"

@suppliers_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('suppliers.login'))
