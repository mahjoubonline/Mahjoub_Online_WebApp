# coding: utf-8
# 🚀 مستند المسارات السيادي لتعميد الموردين والمحافظ - منصة محجوب أونلاين 2026

from flask import request, jsonify, render_template, url_for
from werkzeug.security import generate_password_hash
import random

# استيراد الامتدادات والنماذج الحوكمية بشكل آمن
from apps.extensions import db 
from apps.models.supplier_db import Supplier 
from apps.models.wallet_db import SupplierWallet

# 🛡️ استدعاء الـ Blueprint الجاهز المعرف في ملف __init__.py الخاص بالـ package الحالي
from . import admin_suppliers_bp

# دالة توليد الأرقام المتسلسلة التلقائية لـ (المورد والمحفظة) عبر الـ API
@admin_suppliers_bp.route('/check_duplicate', methods=['GET'])
def check_duplicate():
    check_type = request.args.get('type')
    
    # 1. جلب التسلسل التلقائي الذكي المعتمد لمنصة محجوب أونلاين
    if check_type == 'get_next_sequence':
        try:
            next_supplier_id = Supplier.generate_next_sovereign_id()
            next_wallet_id = SupplierWallet.generate_next_wallet_code()
            
            return jsonify({
                "next_sequence": next_supplier_id,
                "next_wallet": next_wallet_id
            })
            
        except Exception as e:
            return jsonify({"next_sequence": "SUP-MAH9631", "next_wallet": "WEL-MAH9631"})
            
    # 2. التحقق من عدم تكرار اسم المستخدم في قاعدة البيانات
    if check_type == 'username':
        val = request.args.get('value', '').strip()
        exists = Supplier.query.filter_by(username=val).first() is not None
        return jsonify({"exists": exists})
        
    # 3. التحقق من عدم تكرار رقم الوثيقة الشخصية
    if check_type == 'identity_number':
        val = request.args.get('value', '').strip()
        exists = Supplier.query.filter_by(identity_number=val).first() is not None
        return jsonify({"exists": exists})

    return jsonify({"error": "نوع التحقق غير معروف"}), 400


# دالة استقبال الفورم وحفظ المورد والمحفظة بالتزامن المالي الكامل
@admin_suppliers_bp.route('/add_supplier_submit', methods=['POST'])
def add_supplier_submit():
    try:
        # استقبال المعرفات الجوهرية من حقول الواجهة المخفية
        sovereign_id = request.form.get('sovereign_id')
        wallet_code = request.form.get('wallet_code')
        
        if not sovereign_id or not wallet_code:
            sovereign_id = Supplier.generate_next_sovereign_id()
            wallet_code = SupplierWallet.generate_next_wallet_code()

        username = request.form.get('username')
        raw_password = request.form.get('password')
        
        # تشفير كلمة المرور بنظام الهاش الآمن
        password_hash = generate_password_hash(raw_password) if raw_password else "default_hash"
        
        identity_type = request.form.get('identity_type')
        identity_number = request.form.get('identity_number')
        
        owner_name = request.form.get('owner_name')
        trade_name = request.form.get('trade_name')
        shop_number = request.form.get('shop_number')  
        owner_phone = request.form.get('owner_phone')
        
        province = request.form.get('province')
        district = request.form.get('district')
        address_detail = request.form.get('address_detail')
        
        fin_type = request.form.get('fin_type')
        bank_name = request.form.get('bank_name')
        bank_acc = request.form.get('bank_acc')

        # 👑 الخطوة الأولى: إنشاء كائن المورد الجديد
        new_supplier = Supplier(
            sovereign_id=sovereign_id,
            wallet_code=wallet_code,
            username=username,
            password_hash=password_hash,
            identity_type=identity_type,
            identity_number=identity_number,
            owner_name=owner_name,
            owner_phone=owner_phone,
            trade_name=trade_name,
            shop_number=shop_number,
            shop_phone=owner_phone,  
            province=province,
            district=district,
            address_detail=address_detail,
            fin_type=fin_type,
            bank_name=bank_name,
            bank_acc=bank_acc,
            status='active'  
        )
        db.session.add(new_supplier)

        # 💳 الخطوة الثانية: تهيئة وإنشاء المحفظة السيادية المرتبطة به تلقائياً
        new_wallet = SupplierWallet(
            supplier_id=sovereign_id,  
            wallet_code=wallet_code,
            yer_total=0.00, yer_withdrawn=0.00, yer_pending=0.00,
            sar_total=0.00, sar_withdrawn=0.00, sar_pending=0.00,
            usd_total=0.00, usd_withdrawn=0.00, usd_pending=0.00,
            status='نشطة'
        )
        db.session.add(new_wallet)
        
        # إتمام عملية الحفظ المزدوجة الآمنة في الداتابيز
        db.session.commit()
        
        return jsonify({
            "status": "success", 
            "message": f"تم تعميد المورد بنجاح بالمعرف {sovereign_id} وإنشاء محفظته الموحدة رقم {wallet_code}"
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": f"خطأ سيادي أثناء الحفظ المالي: {str(e)}"})
