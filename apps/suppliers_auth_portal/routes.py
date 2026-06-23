# coding: utf-8
# 📂 apps/suppliers_auth_portal/routes.py - نظام الدخول السيادي (نسخة معزولة ومحمية)

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from flask_login import login_user, logout_user, current_user
from apps.extensions import db  # تم التعديل لتستخدم الامتداد الصحيح للنظام الموحد
import uuid

# تعريف الـ Blueprint باسم 'suppliers'
suppliers_bp = Blueprint('suppliers', __name__, template_folder='templates')

@suppliers_bp.before_request
def check_login():
    """حماية سيادية: فحص الحماية فقط إذا كان الطلب يخص مستخدم غير مسجل وموجه لهذا الـ Blueprint"""
    # استثناء ملفات الستاتيك وصفحة اللوجن لمنع التكرار اللانهائي
    if request.endpoint in ['suppliers.login', 'static'] or not request.blueprint == 'suppliers':
        return None
    
    # استثناء لوحة تحكم المسوقين إذا كانت تتبع موديول آخر
    if request.endpoint and 'marketers' in request.endpoint:
        return None

    if not current_user.is_authenticated:
        return redirect(url_for('suppliers.login'))

@suppliers_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            # إذا كان مسجلاً بالفعل، وجهه للوحة التحكم فوراً بدل حظره
            return redirect(url_for('suppliers.dashboard'))
        return render_template('suppliers_auth_portal/login.html')

    # استيراد النماذج (Model imports) - آمنة ومحدثة
    from apps.models.otp_db import OTPVerification
    from apps.models.admin_db import AdminUser # للتأكد من عدم التداخل مع الجلسات الإدارية

    # ملاحظة: قم بتعديل مسارات الـ Models حسب أسماء ملفات الموردين والمسوقين لديك إذا لزم الأمر
    try:
        # فحص إذا كان الطلب قادم كـ JSON (واجهات حديثة) أو Form عادي
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        if not data:
            return jsonify({"status": "error", "message": "بيانات غير صالحة"}), 400

        login_type = data.get('type')
        
        # --- دخول المسوقين ---
        if login_type == 'marketer':
            username = data.get('username', '').strip()
            password = data.get('password', '')
            
            # استيراد نموذج المسوقين هنا لحماية الذاكرة
            from apps.models import Marketer
            user = Marketer.query.filter_by(marketing_code=username).first()
            if user and hasattr(user, 'check_password') and user.check_password(password): 
                login_user(user, remember=True)
                return jsonify({"status": "success", "redirect": url_for('marketers.dashboard')})
            return jsonify({"status": "error", "message": "بيانات الدخول غير صحيحة"}), 401

        # --- دخول الموردين (رقم الهاتف + OTP) ---
        raw_phone = data.get('phone', '')
        phone = "".join(filter(str.isdigit, raw_phone))
        otp = data.get('otp')

        if not phone:
            return jsonify({"status": "error", "message": "رقم الهاتف مطلوب"}), 400

        # خطوة 1: طلب توليد وإرسال الـ OTP
        if phone and not otp:
            # تعديل الرقم لتبدأ بالصيغة الدولية المتوافقة مع الـ API
            if len(phone) == 9 and phone.startswith('7'):
                phone = '967' + phone
            elif len(phone) == 10 and phone.startswith('07'):
                phone = '967' + phone[1:]

            # توليد الرمز (سيستخدم الـ Dispatcher الافتراضي للموردين المربوط في otp_db تلقائياً)
            new_otp = OTPVerification.generate_otp(phone)
            if new_otp:
                print(f"🔐 [Supplier OTP] تم توليد رمز للمورد: {phone}")
                return jsonify({"status": "success", "message": "تم إرسال رمز التحقق بنجاح عبر الواتساب"})
            return jsonify({"status": "error", "message": "فشل إرسال الرمز، يرجى المحاولة لاحقاً"}), 500

        # خطوة 2: التحقق الفعلي وتسجيل الدخول
        if phone and otp:
            if len(phone) == 9 and phone.startswith('7'):
                phone = '967' + phone
            elif len(phone) == 10 and phone.startswith('07'):
                phone = '967' + phone[1:]

            if OTPVerification.verify_otp(phone, otp):
                from apps.models import Supplier
                supplier = Supplier.query.filter_by(phone=phone).first()
                
                # إذا كان المورد جديداً، يتم إنشاؤه تلقائياً لسهولة الانضمام لشركاء النجاح
                if not supplier:
                    supplier = Supplier(
                        username=f"supplier_{uuid.uuid4().hex[:8]}",
                        supplier_code=f"VEN-{uuid.uuid4().hex[:6].upper()}",
                        phone=phone, 
                        trade_name="مورد جديد لدينا"
                    )
                    db.session.add(supplier)
                    db.session.commit()
                
                login_user(supplier, remember=True)
                session.permanent = True
                return jsonify({"status": "success", "redirect": url_for('suppliers.dashboard')})
            
            return jsonify({"status": "error", "message": "رمز التحقق منتهي أو خاطئ"}), 400

        return jsonify({"status": "error", "message": "بيانات غير مكتملة"}), 400

    except Exception as e:
        db.session.rollback()
        print(f"🚨 [Supplier Auth Error]: {str(e)}")
        return jsonify({"status": "error", "message": "حدث خطأ فني في خادم المصادقة"}), 500

@suppliers_bp.route('/dashboard')
def dashboard():
    return "مرحباً بك في لوحة تحكم الموردين لمنصة محجوب أونلاين"

@suppliers_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('suppliers.login'))
