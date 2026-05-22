# coding: utf-8
# 🚀 مستند المسارات السيادي لتعميد الموردين والمحافظ - منصة محجوب أونلاين 2026

from flask import request, jsonify, render_template, url_for, redirect
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user

# 🛡️ استدعاء الـ Blueprint الجاهز والمثبت للتطبيق المصغر
from . import admin_suppliers_bp

# ========================================================
# 🏬 النافذة الأساسية: عرض تطبيق "تسجيل المورد" كصفحة كاملة مستقلة
# ========================================================
@admin_suppliers_bp.route('/register', methods=['GET'])
@login_required
def add_supplier_page():
    try:
        from apps.models.supplier_db import Supplier
        from apps.models.wallet_db import SupplierWallet
        
        # توليد الأرقام المتسلسلة التلقائية لتجهيزها في حقول النافذة المستقلة
        next_supplier_id = Supplier.generate_next_sovereign_id()
        next_wallet_id = SupplierWallet.generate_next_wallet_code()
        
        # تحويل المسؤول إلى واجهة القالب المستقلة للتطبيق المصغر بالكامل
        return render_template('admin/add_supplier.html', 
                               current_user=current_user,
                               next_sequence=next_supplier_id,
                               next_wallet=next_wallet_id)
    except Exception as e:
        return f"خطأ في تحميل نافذة تطبيق الموردين: {str(e)}", 500


# ========================================================
# 🧠 دالة فحص وتوليد الأرقام المتسلسلة التلقائية عبر الـ API للتطبيق
# ========================================================
@admin_suppliers_bp.route('/check_duplicate', methods=['GET'])
def check_duplicate():
    check_type = request.args.get('type')
    from apps.models.supplier_db import Supplier 
    from apps.models.wallet_db import SupplierWallet
    
    if check_type == 'get_next_sequence':
        try:
            next_supplier_id = Supplier.generate_next_sovereign_id()
            next_wallet_id = SupplierWallet.generate_next_wallet_code()
            return jsonify({"next_sequence": next_supplier_id, "next_wallet": next_wallet_id})
        except Exception:
            return jsonify({"next_sequence": "SUP-MAH9631", "next_wallet": "WEL-MAH9631"})
            
    if check_type == 'username':
        val = request.args.get('value', '').strip()
        return jsonify({"exists": Supplier.query.filter_by(username=val).first() is not None})
        
    if check_type == 'identity_number':
        val = request.args.get('value', '').strip()
        return jsonify({"exists": Supplier.query.filter_by(identity_number=val).first() is not None})

    return jsonify({"error": "نوع التحقق غير معروف"}), 400


# ========================================================
# 💳 دالة استقبال الحفظ والتزامن المالي للمحفظة والمورد
# ========================================================
@admin_suppliers_bp.route('/add_supplier_submit', methods=['POST'])
@login_required
def add_supplier_submit():
    try:
        from apps.extensions import db 
        from apps.models.supplier_db import Supplier 
        from apps.models.wallet_db import SupplierWallet

        sovereign_id = request.form.get('sovereign_id')
        wallet_code = request.form.get('wallet_code')
        
        if not sovereign_id or not wallet_code:
            sovereign_id = Supplier.generate_next_sovereign_id()
            wallet_code = SupplierWallet.generate_next_wallet_code()

        username = request.form.get('username')
        raw_password = request.form.get('password')
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

        new_supplier = Supplier(
            sovereign_id=sovereign_id, wallet_code=wallet_code, username=username,
            password_hash=password_hash, identity_type=identity_type, identity_number=identity_number,
            owner_name=owner_name, owner_phone=owner_phone, trade_name=trade_name,
            shop_number=shop_number, shop_phone=owner_phone, province=province,
            district=district, address_detail=address_detail, fin_type=fin_type,
            bank_name=bank_name, bank_acc=bank_acc, status='active'  
        )
        db.session.add(new_supplier)

        new_wallet = SupplierWallet(
            supplier_id=sovereign_id, wallet_code=wallet_code,
            yer_total=0.00, yer_withdrawn=0.00, yer_pending=0.00,
            sar_total=0.00, sar_withdrawn=0.00, sar_
