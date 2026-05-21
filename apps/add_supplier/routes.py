# coding: utf-8
# 🛡️ وحدة تعميد الموردين - منصة محجوب أونلاين 2026

from flask import Blueprint, render_template, request, jsonify, url_for
from flask_login import login_required
from apps import db
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import SupplierWallet
import uuid
import secrets
import string

# تعريف الـ Blueprint
admin_suppliers_bp = Blueprint('add_supplier', __name__, template_folder='templates')

def generate_sovereign_id():
    """توليد معرف سيادي فريد للمورد"""
    random_part = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    return f"SUP-MAH{random_part}"

def generate_wallet_code(supplier_id):
    """توليد كود محفظة مرتبط بمعرف المورد"""
    return supplier_id.replace("SUP-", "WEL-")

@admin_suppliers_bp.route('/add', methods=['GET'])
@login_required
def add_supplier_page():
    """عرض صفحة استمارة تعميد المورد"""
    return render_template('add_supplier.html')

@admin_suppliers_bp.route('/check-duplicate', methods=['GET'])
@login_required
def check_duplicate():
    """التحقق من تكرار البيانات أو جلب التسلسل القادم"""
    check_type = request.args.get('type')
    value = request.args.get('value')

    if check_type == 'get_next_sequence':
        return jsonify({"next_sequence": generate_sovereign_id()})

    exists = False
    if check_type == 'username':
        exists = Supplier.query.filter_by(username=value).first() is not None
    elif check_type == 'identity_number':
        exists = Supplier.query.filter_by(identity_number=value).first() is not None
    elif check_type == 'owner_phone':
        exists = Supplier.query.filter_by(owner_phone=value).first() is not None
    elif check_type == 'trade_name':
        exists = Supplier.query.filter_by(trade_name=value).first() is not None
    elif check_type == 'bank_acc':
        exists = Supplier.query.filter_by(bank_acc=value).first() is not None

    return jsonify({"exists": exists})

@admin_suppliers_bp.route('/submit', methods=['POST'])
@login_required
def add_supplier_submit():
    """معالجة حفظ المورد الجديد في قاعدة البيانات السيادية"""
    try:
        # توليد المعرفات
        sovereign_id = generate_sovereign_id()
        wallet_code = generate_wallet_code(sovereign_id)

        # استقبال البيانات
        new_supplier = Supplier(
            sovereign_id=sovereign_id,
            wallet_code=wallet_code,
            username=request.form.get('username'),
            password=request.form.get('password'), # يجب تشفيرها في مرحلة الإنتاج
            identity_type=request.form.get('identity_type'),
            identity_number=request.form.get('identity_number'),
            owner_name=request.form.get('owner_name'),
            trade_name=request.form.get('trade_name'),
            owner_phone=request.form.get('owner_phone'),
            shop_phone=request.form.get('shop_phone'),
            province=request.form.get('province'),
            district=request.form.get('district'),
            address_detail=request.form.get('address_detail'),
            bank_name=request.form.get('bank_name'),
            bank_acc=request.form.get('bank_acc'),
            activity_type=request.form.get('activity_type')
        )

        # إنشاء المحفظة المرتبطة
        new_wallet = SupplierWallet(
            wallet_code=wallet_code,
            supplier_id=sovereign_id,
            status='نشطة'
        )

        db.session.add(new_supplier)
        db.session.add(new_wallet)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "تم تعميد المورد بنجاح",
            "data": {
                "sovereign_id": sovereign_id,
                "wallet_code": wallet_code
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
