# coding: utf-8
# 📂 apps/wallet/routes.py - النسخة النهائية المتكاملة

from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required
from apps.extensions import db
from apps.models.wallet_db import SupplierWallet, WalletTransaction

# تعريف الـ Blueprint
wallet_app = Blueprint(
    'wallet_app', 
    __name__, 
    template_folder='templates'
)

# 1. عرض لوحة تحكم المحفظة (الرئيسية)
@wallet_app.route('/dashboard')
@login_required
def wallet_dashboard():
    try:
        # حساب الإجماليات للنظام
        total_sar = db.session.query(db.func.sum(SupplierWallet.balance_sar)).scalar()
        total_yer = db.session.query(db.func.sum(SupplierWallet.balance_yer)).scalar()
        total_usd = db.session.query(db.func.sum(SupplierWallet.balance_usd)).scalar()
        
        # تحويل النتائج لـ float وتجنب القيم الفارغة (None)
        total_system_sar = float(total_sar) if total_sar else 0.0
        total_system_yer = float(total_yer) if total_yer else 0.0
        total_system_usd = float(total_usd) if total_usd else 0.0
        
    except Exception as e:
        print(f"DEBUG: Error in wallet_dashboard: {e}")
        total_system_sar = total_system_yer = total_system_usd = 0.0
    
    return render_template(
        'admin/wallet_app.html', 
        total_system_sar=total_system_sar,
        total_system_yer=total_system_yer,
        total_system_usd=total_system_usd
    )

# 2. عرض محفظة مورد محدد (يتم استدعاؤها عبر AJAX/Fetch)
@wallet_app.route('/view/<int:supplier_id>')
@login_required
def view_wallet(supplier_id):
    # جلب المحفظة
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier_id).first()
    
    if wallet:
        wallet.balance_sar = float(wallet.balance_sar)
        wallet.balance_yer = float(wallet.balance_yer)
        wallet.balance_usd = float(wallet.balance_usd)
    
    # الحصول على رقم الصفحة
    page = request.args.get('page', 1, type=int)
    
    transactions_pagination = None
    transactions = []
    
    if wallet:
        # جلب العمليات مع ترقيم الصفحات
        transactions_pagination = WalletTransaction.query.filter_by(wallet_id=wallet.id)\
            .order_by(WalletTransaction.created_at.desc())\
            .paginate(page=page, per_page=10, error_out=False)
        
        transactions = transactions_pagination.items
        
        # تحويل مبالغ العمليات إلى float
        for tx in transactions:
            tx.amount = float(tx.amount)
    
    return render_template(
        'admin/view_wallet.html', 
        wallet=wallet, 
        transactions=transactions,
        pagination=transactions_pagination
    )

# 3. معالجة العمليات المالية (إيداع / سحب)
@wallet_app.route('/add_transaction', methods=['POST'])
@login_required
def add_transaction():
    try:
        data = request.json
        wallet_id = data.get('wallet_id')
        amount = float(data.get('amount', 0))
        tx_type = data.get('type')  # إيداع أو سحب
        description = data.get('description', '')

        # تحديث الرصيد (منطق مبدئي)
        wallet = SupplierWallet.query.get(wallet_id)
        if not wallet:
            return jsonify({"status": "error", "message": "المحفظة غير موجودة"}), 404

        # إضافة العملية
        new_tx = WalletTransaction(
            wallet_id=wallet.id,
            amount=amount,
            type=tx_type,
            description=description
        )
        db.session.add(new_tx)
        
        # منطق تحديث الرصيد هنا ...
        # (سيتم ربطه بـ DB لاحقاً)
        
        db.session.commit()
        return jsonify({"status": "success", "message": "تمت العملية بنجاح"})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 400
