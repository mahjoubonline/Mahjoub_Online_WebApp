# coding: utf-8
# 🚀 مستند المسارات السيادي لتطبيق تعميد الموردين - منصة محجوب أونلاين 2026

from flask import request, jsonify, render_template
from werkzeug.security import generate_password_hash
from flask_login import login_required

from . import admin_suppliers_bp

# ========================================================
# 🏬 المسار الأول (GET): يرجع محتوى الاستمارة الصافي فقط لحقنه بالهيكل
# ========================================================
@admin_suppliers_bp.route('/add_supplier', methods=['GET'])
@login_required
def add_supplier_page():
    try:
        from apps.models.supplier_db import Supplier
        from apps.models.wallet_db import SupplierWallet
        
        # توليد المعرفات المتسلسلة تلقائياً لتجهيزها داخل الحقول
        next_supplier_id = Supplier.generate_next_sovereign_id()
        next_wallet_id = SupplierWallet.generate_next_wallet_code()
        
        # نرجع القالب الفرعي الصافي والمجرد لكي يتم حقنه صامتاً داخل الهيكل الأساسي
        return render_template('admin/add_supplier.html', 
                               next_sequence=next_supplier_id,
                               next_wallet=next_wallet_id)
    except Exception as e:
        return f"<div class='alert alert-danger'>خطأ في تحميل الاستمارة: {str(e)}</div>", 500


# ========================================================
# 💳 المسار الثاني (POST): مخصص فقط لاستقبال البيانات وحفظها في قاعدة البيانات
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
            sar_total=0.00, sar_withdrawn=0.00, sar_pending=0.00,
            usd_total=0.00, usd_withdrawn=0.00, usd_pending=0.00, status='نشطة'
        )
        db.session.add(new_wallet)
        db.session.commit()
        
        return jsonify({
            "status": "success", 
            "message": f"تم تعميد المورد بنجاح بالمعرف {sovereign_id}"
        })

    except Exception as e:
        from apps.extensions import db
        db.session.rollback()
        return jsonify
