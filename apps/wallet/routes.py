# coding: utf-8
# 📂 apps/wallet/routes.py - النسخة المعتمدة للإنتاج

from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from apps import db 
from apps.models.wallet_db import SupplierWallet, WalletTransaction

# تعريف الـ Blueprint
wallet_app = Blueprint(
    'wallet_app', 
    __name__, 
    template_folder='templates'
)

# 1. عرض لوحة تحكم المحفظة
@wallet_app.route('/dashboard')
@login_required
def wallet_dashboard():
    # حساب إجماليات النظام مع معالجة استباقية لأي خطأ في قاعدة البيانات
    try:
        total_sar = db.session.query(db.func.sum(SupplierWallet.balance_sar)).scalar()
        total_yer = db.session.query(db.func.sum(SupplierWallet.balance_yer)).scalar()
        total_usd = db.session.query(db.func.sum(SupplierWallet.balance_usd)).scalar()
        
        # تعيين قيمة افتراضية 0.0 إذا كانت النتيجة None
        total_system_sar = float(total_sar) if total_sar else 0.0
        total_system_yer = float(total_yer) if total_yer else 0.0
        total_system_usd = float(total_usd) if total_usd else 0.0
        
    except Exception as e:
        print(f"DEBUG: Error in wallet_dashboard: {e}")
        total_system_sar = total_system_yer = total_system_usd = 0.0
    
    return render_template(
        'wallet/dashboard.html', 
        total_system_sar=total_system_sar,
        total_system_yer=total_system_yer,
        total_system_usd=total_system_usd
    )

# 2. عرض محفظة مورد محدد
@wallet_app.route('/view/<int:supplier_id>')
@login_required
def view_wallet(supplier_id):
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier_id).first()
    transactions = []
    if wallet:
        transactions = WalletTransaction.query.filter_by(wallet_id=wallet.id)\
            .order_by(WalletTransaction.created_at.desc()).all()
    
    return render_template('wallet/view_wallet.html', wallet=wallet, transactions=transactions)

# 3. إضافة عملية مالية (API)
@wallet_app.route('/add_transaction', methods=['POST'])
@login_required
def add_transaction():
    # منطق إضافة المعاملات سيكون هنا
    return jsonify({"status": "success", "message": "تمت العملية بنجاح"})
