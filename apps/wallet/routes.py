# coding: utf-8
# 📂 apps/wallet/routes.py

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from apps.models.wallet_db import SupplierWallet, WalletTransaction
from apps.models.supplier_db import Supplier
from apps.extensions import db
from sqlalchemy import or_
from decimal import Decimal

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
        'total_sar': db.session.query(db.func.sum(SupplierWallet.balance_sar)).scalar() or 0,
        'total_yer': db.session.query(db.func.sum(SupplierWallet.balance_yer)).scalar() or 0,
        'total_usd': db.session.query(db.func.sum(SupplierWallet.balance_usd)).scalar() or 0
    }
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('admin/partials/wallet_table_body.html', wallets=wallets.items, pagination=wallets)
    return render_template('admin/wallet_app.html', wallets=wallets.items, total_sar=stats['total_sar'], total_yer=stats['total_yer'], total_usd=stats['total_usd'], pagination=wallets)

@wallet_bp.route('/admin/manage/<int:supplier_id>', methods=['GET'])
@login_required
def manage_wallet(supplier_id):
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier_id).first_or_404()
    return render_template('admin/view_wallet.html', wallet=wallet)

@wallet_bp.route('/admin/manage/<int:supplier_id>/add_transaction', methods=['POST'])
@login_required
def add_transaction(supplier_id):
    """إضافة حركة مالية باستخدام المحرك الرشيق الموحد."""
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier_id).first_or_404()
    
    try:
        amount = Decimal(request.form.get('amount', 0))
        trans_type = request.form.get('type') # credit / debit
        order_ref = request.form.get('reference_number', '').strip()
        
        if amount <= 0:
            flash("يجب أن يكون المبلغ أكبر من صفر.", "danger")
            return redirect(url_for('wallet_app.manage_wallet', supplier_id=supplier_id))

        # تنفيذ العملية عبر المحرك المالي في wallet_db.py
        new_trans = WalletTransaction.execute_transfer(
            wallet_id=wallet.id,
            amount=amount,
            trans_type=trans_type,
            owner_type='supplier',
            owner_id=wallet.supplier_id,
            description=f"عملية مالية للطلب رقم {order_ref}"
        )
        
        # تحديث بيانات إضافية للحركة
        new_trans.currency = request.form.get('currency', 'SAR')
        new_trans.related_order_id = order_ref
        new_trans.reference_number = order_ref
        
        db.session.commit()
        flash(f"تم تسجيل العملية للطلب {order_ref} بنجاح.", "success")
        
    except Exception as e:
        db.session.rollback()
        flash(f"حدث خطأ تقني: {str(e)}", "danger")

    return redirect(url_for('wallet_app.manage_wallet', supplier_id=supplier_id))
