# coding: utf-8
# 📂 apps/wallet/routes.py

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from apps.models.wallet_db import SupplierWallet, WalletTransaction
from apps.models.supplier_db import Supplier
from apps.extensions import db
from sqlalchemy import or_

# تأكد أن اسم الـ Blueprint هنا يطابق ما يتم استدعاؤه في القوالب
wallet_bp = Blueprint('wallet_app', __name__, template_folder='templates')

@wallet_bp.route('/admin/dashboard', methods=['GET'])
@login_required
def dashboard():
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)

    query = SupplierWallet.query.join(Supplier, SupplierWallet.supplier_id == Supplier.id)
    
    if search:
        query = query.filter(or_(
            Supplier.trade_name.ilike(f'%{search}%'),
            SupplierWallet.wallet_code.ilike(f'%{search}%')
        ))

    wallets = query.paginate(page=page, per_page=20, error_out=False)
    
    stats = {
        'count': SupplierWallet.query.count(),
        'sar': db.session.query(db.func.sum(SupplierWallet.balance_sar)).scalar() or 0,
        'yer': db.session.query(db.func.sum(SupplierWallet.balance_yer)).scalar() or 0,
        'usd': db.session.query(db.func.sum(SupplierWallet.balance_usd)).scalar() or 0
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('admin/partials/wallet_table_body.html', wallets=wallets.items, pagination=wallets)

    return render_template('admin/wallet_app.html', wallets=wallets.items, stats=stats, pagination=wallets)

@wallet_bp.route('/admin/manage/<int:supplier_id>', methods=['GET'])
@login_required
def manage_wallet(supplier_id):
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier_id).first_or_404()
    return render_template('admin/view_wallet.html', wallet=wallet)

@wallet_bp.route('/admin/manage/<int:supplier_id>/add_transaction', methods=['POST'])
@login_required
def add_transaction(supplier_id):
    """
    إضافة سند تسوية يدوي مع تمييز مصدر الحركة والتأكد من الرصيد
    """
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier_id).first_or_404()
    
    amount = float(request.form.get('amount', 0))
    trans_type = request.form.get('type')  # 'credit' أو 'debit'
    currency = request.form.get('currency')
    ref = request.form.get('reference_number')
    desc = request.form.get('description')

    # 1. التحقق من صحة المبلغ
    if amount <= 0:
        flash("يجب أن يكون المبلغ أكبر من صفر.", "danger")
        return redirect(url_for('wallet_app.manage_wallet', supplier_id=supplier_id))

    try:
        # 2. [تحسين محاسبي]: التأكد من توفر رصيد قبل السحب
        if trans_type == 'debit':
            if currency == 'SAR' and wallet.balance_sar < amount:
                flash("رصيد SAR غير كافٍ للعملية.", "danger")
                return redirect(url_for('wallet_app.manage_wallet', supplier_id=supplier_id))
            if currency == 'YER' and wallet.balance_yer < amount:
                flash("رصيد YER غير كافٍ للعملية.", "danger")
                return redirect(url_for('wallet_app.manage_wallet', supplier_id=supplier_id))
            if currency == 'USD' and wallet.balance_usd < amount:
                flash("رصيد USD غير كافٍ للعملية.", "danger")
                return redirect(url_for('wallet_app.manage_wallet', supplier_id=supplier_id))

        # 3. تحديث رصيد المحفظة بناءً على العملة
        if currency == 'SAR':
            wallet.balance_sar += amount if trans_type == 'credit' else -amount
        elif currency == 'YER':
            wallet.balance_yer += amount if trans_type == 'credit' else -amount
        elif currency == 'USD':
            wallet.balance_usd += amount if trans_type == 'credit' else -amount

        # 4. إنشاء قيد الحركة (سند تسوية)
        new_trans = WalletTransaction(
            wallet_id=wallet.id,
            trans_type=trans_type,
            source_type='voucher',
            amount=amount,
            currency=currency,
            reference_number=ref,
            description=desc
        )
        
        db.session.add(new_trans)
        db.session.commit()
        flash(f"تم تسجيل السند {ref} بنجاح.", "success")
        
    except Exception as e:
        db.session.rollback()
        flash("حدث خطأ تقني أثناء معالجة السند.", "danger")

    return redirect(url_for('wallet_app.manage_wallet', supplier_id=supplier_id))
