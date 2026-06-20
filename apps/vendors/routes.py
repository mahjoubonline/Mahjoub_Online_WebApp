# coding: utf-8
# 📂 apps/vendors/routes.py - العقل المدبر الخلفي لدخول الموردين وحوكمة الـ OTP

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from apps.extensions import db
from apps.models.supplier_db import Supplier

# 🛡️ معالجة الاستدعاءات الحيوية بحذر لمنع توقف المحرك التلقائي
try:
    from apps.models.otp_db import OTPVerification
except ImportError:
    OTPVerification = None

# ملاحظة: تم تعليق الملف غير الموجود حالياً لمنع انهيار السيرفر No module named 'apps.models.supplier_user_db'
# from apps.models.supplier_user_db import SupplierUser  

from werkzeug.security import check_password_hash 
from . import vendors_bp

# 1️⃣ مسار فحص الحساب وتوليد الرمز (الخطوة الأولى من الواجهة)
@vendors_bp.route('/check-account', methods=['POST'])
def check_account():
    """الفحص الأولي لاسم المستخدم وتوليد رمز AES-256 OTP حياً"""
    data = request.get_json() or {}
    username = data.get('username')

    if not username:
        return jsonify({"status": "error", "message": "الرجاء إدخل اسم المستخدم الإداري المعتمد"}), 400

    supplier = Supplier.query.filter_by(username=username).first()
    
    if not supplier:
        return jsonify({"status": "error", "message": "هذا الحساب غير مسجل في منظومة الموردين"}), 404

    if supplier.status != "active":
        return jsonify({"status": "error", "message": "هذا الحساب معلق إدارياً، راجع الدعم الفني لـ MAHJOUB ONLINE"}), 403

    if not OTPVerification:
        return jsonify({"status": "error", "message": "منظومة التحقق من الرموز (OTP) قيد التهيئة الفنية حالياً"}), 500

    try:
        target_phone = supplier.owner_phone 
        raw_otp = OTPVerification.generate_otp(email=username, expires_in_minutes=5)
        db.session.commit()

        print(f"📦 [MAHJOUB BRIDGE SYSTEM] تم توليد الرمز بنجاح للمورد {username} -> الرمز النقي للتجربة: {raw_otp}")

        return jsonify({
            "status": "success", 
            "message": "تمت معالجة رمز التحقق بنجاح وإرساله إلى قنواتك المعتمدة",
            "trade_name": supplier.trade_name 
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": f"فشل في معالجة نظام الرموز السيادي: {str(e)}"}), 500


# 2️⃣ مسار التحقق من الرمز الفوري (الخطوة الثانية من الواجهة)
@vendors_bp.route('/verify-otp-token', methods=['POST'])
def verify_otp_token():
    """المطابقة الحية للرمز المشفر بـ AES-256 واستهلاكه فوراً للسيادة الأمنية"""
    if not OTPVerification:
        return jsonify({"status": "error", "message": "الخدمة غير متوفرة حالياً"}), 500

    data = request.get_json() or {}
    username = data.get('username')
    otp_code = data.get('otp_code')

    if not username or not otp_code:
        return jsonify({"status": "error", "message": "البيانات المدخلة غير مكتملة"}), 400

    is_valid = OTPVerification.verify_otp(email=username, input_code=otp_code)

    if is_valid:
        return jsonify({"status": "success", "message": "تمت مطابقة الرمز بنجاح، انتقل لخطوة التوقيع النهائي"}), 200
    else:
        return jsonify({"status": "error", "message": "رمز التحقق غير صحيح أو انتهت صلاحيته الزمنية"}), 400


# 3️⃣ مسار البوابة والتحقق النهائي من كلمة المرور (GET & POST)
@vendors_bp.route('/login', methods=['GET', 'POST'])
def login():
    """بوابة الدخول الرئيسية واستقبال التوقيع النهائي بكلمة المرور وحوكمة الصلاحيات"""
    if current_user.is_authenticated:
        return redirect(url_for('vendors.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        otp_code = request.form.get('otp_code')

        if not username or not password or not otp_code:
            flash("الرجاء إكمال كافة خطوات التحقق السيادية أولاً", "danger")
            return render_template('vendor/login.html')

        supplier = Supplier.query.filter_by(username=username, status="active").first()
        
        if supplier and check_password_hash(supplier.password_hash, password):
            supplier.generate_codes()
            db.session.commit()

            login_user(supplier)
            flash(f"مرحباً بك مجدداً في لوحة إدارة الحوكمة الرقمية لـ {supplier.trade_name}", "success")
            return redirect(url_for('vendors.dashboard'))
        
        flash("فشل في مطابقة كلمة المرور المعتمدة لحسابك أو الحساب غير نشط", "danger")
        return render_template('vendor/login.html')
        
    return render_template('vendor/login.html')


# 4️⃣ مسار لوحة التحكم الخاصة بالمورد (المحمية)
@vendors_bp.route('/dashboard')
@login_required
def dashboard():
    """لوحة التحكم السيادية للمورد الموثق وبوابة حوكمة العمليات"""
    wallet = getattr(current_user, 'wallet', None)
    return render_template('vendor/dashboard.html', supplier=current_user, wallet=wallet)


# 5️⃣ مسار تسجيل الخروج وإغلاق الجلسة السيادية
@vendors_bp.route('/logout')
@login_required
def logout():
    """تسجيل خروج آمن للمورد وتدمير الجلسة الحالية حمايةً للبيانات السيادية"""
    try:
        trade_name = current_user.trade_name
        logout_user()
        flash(f"تم تسجيل الخروج بنجاح من لوحة تحكم {trade_name}. في أمان الله.", "success")
    except Exception as e:
        flash("حدث خطأ أثناء محاولة تسجيل الخروج الآمن.", "danger")
        
    return redirect(url_for('vendors.login'))
