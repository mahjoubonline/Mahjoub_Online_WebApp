# coding: utf-8
# 📂 apps/vendors/routes.py

from flask import Blueprint, request, jsonify, session
from apps.extensions import db
from apps.models.supplier_db import Supplier
from apps.models.supplier_profile_db import SupplierProfile
from apps.vendors.vendor_auth_service import trigger_otp_process, verify_vendor_otp
from werkzeug.security import generate_password_hash, check_password_hash

vendors_bp = Blueprint('vendors', __name__)

@vendors_bp.route('/auth-gateway', methods=['POST'])
def auth_gateway():
    """بوابة ذكية: تتعرف على حالة الشريك (قديم/جديد)"""
    data = request.get_json()
    email = data.get('email')
    phone = data.get('phone')
    
    # البحث عن المورد (يتم فك التشفير عبر الـ getter في الموديل)
    supplier = Supplier.query.filter_by(_owner_email=email).first() 
    
    if supplier:
        # شريك مسجل: نرسل OTP للدخول
        trigger_otp_process(email, phone)
        return jsonify({"status": "existing_user", "message": "تم العثور على حسابك، يرجى إدخال الرمز المرسل"})
    else:
        # شريك جديد: توجيه لبدء عملية التسجيل
        return jsonify({"status": "new_partner", "message": "مرحباً بك كشريك جديد"})

@vendors_bp.route('/register-complete', methods=['POST'])
def register_complete():
    """إتمام عملية التسجيل وحفظ البيانات المشفرة"""
    data = request.get_json()
    
    try:
        # 1. إنشاء المورد الأساسي (بيانات الاعتماد)
        new_supplier = Supplier(
            username=data['username'],
            owner_email=data['email'],
            owner_phone=data['phone'],
            password_hash=generate_password_hash(data['password']),
            trade_name=data['trade_name']
        )
        new_supplier.generate_codes()
        db.session.add(new_supplier)
        db.session.flush() # للحصول على الـ ID قبل الالتزام
        
        # 2. إنشاء الملف التجاري المتقدم (بيانات مشفرة سيادياً)
        new_profile = SupplierProfile(
            user_id=new_supplier.id,
            trade_name=data['trade_name'],
            owner_name=data['owner_name'],
            bank_acc=data['bank_acc']
        )
        db.session.add(new_profile)
        db.session.commit()
        
        # 3. تفعيل عملية التحقق عبر الواتساب
        trigger_otp_process(data['email'], data['phone'])
        
        return jsonify({"status": "success", "message": "تم إنشاء حسابك، بانتظار التحقق من واتساب"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

@vendors_bp.route('/verify-otp', methods=['POST'])
def verify():
    """التحقق النهائي من هوية الشريك"""
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')
    
    if verify_vendor_otp(email, otp):
        # تفعيل الجلسة للوصول إلى النظام
        session['vendor_authenticated'] = True
        session['vendor_email'] = email
        return jsonify({"status": "success", "redirect": "/vendors/dashboard"})
    
    return jsonify({"status": "error", "message": "رمز التحقق غير صحيح أو منتهي الصلاحية"}), 400
