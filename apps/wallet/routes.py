# coding: utf-8
# 📂 apps/wallet/routes.py - منطق عمليات المحفظة

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from apps.extensions import db
from .models import SupplierWallet, WalletTransaction # تأكد من أنك تستورد النماذج من مكانها الصحيح

# تعريف الـ Blueprint الخاص بالمحفظة
wallet_app = Blueprint(
    'wallet_app', 
    __name__, 
    template_folder='templates'
)

# 1. عرض محفظة المورد
@wallet_app.route('/dashboard')
@login_required
def wallet_dashboard():
    # هنا جلب بيانات المحفظة الخاصة بالمورد الحالي
    wallet = SupplierWallet.query.filter_by(supplier_id=current_user.id).first()
    transactions = WalletTransaction.query.filter_by(wallet_id=wallet.id).order_by(WalletTransaction.created_at.desc()).all() if wallet else []
    
    return render_template('wallet/dashboard.html', wallet=wallet, transactions=transactions)

# 2. إضافة عملية مالية (مثال على مسار داخلي)
@wallet_app.route('/add_transaction', methods=['POST'])
@login_required
def add_transaction():
    # منطق إضافة عملية مالية
    # ...
    return jsonify({"status": "success", "message": "تمت العملية بنجاح"})

# 3. أي مسارات أخرى خاصة بالمحفظة
# @wallet_app.route('/withdraw', ...)
# ...
