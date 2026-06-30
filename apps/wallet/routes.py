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
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier_id).first_or_404()
    
    try:
        # استخدام Decimal للدقة المحاسبية
        amount = Decimal(request.form.get('amount', 0))
        trans_type = request.form.get('type')
        currency = request.form.get('currency')
        order_ref = request.form.get('reference_number', '').strip() # رقم الطلب الفعلي (MJ-...)

        if amount <= 0:
            flash("يجب أن يكون المبلغ أكبر من صفر.", "danger")
            return redirect(url_for('wallet_app.manage_wallet', supplier_id=supplier_id))

        # تحديد الرصيد قبل العملية
        if currency == 'SAR': balance_before = wallet.balance_sar
        elif currency == 'YER': balance_before = wallet.balance_yer
        else: balance_before = wallet.balance_usd

        # التأكد من كفاية الرصيد للعمليات المدينة
        if trans_type == 'debit' and balance_before < amount:
            flash("رصيد العملة غير كافٍ للعملية.", "danger")
            return redirect(url_for('wallet_app.manage_wallet', supplier_id=supplier_id))

        # تحديث رصيد المحفظة
        adjustment = amount if trans_type == 'credit' else -amount
        if currency == 'SAR': wallet.balance_sar += adjustment
        elif currency == 'YER': wallet.balance_yer += adjustment
        elif currency == 'USD': wallet.balance_usd += adjustment
        
        balance_after = balance_before + adjustment

        # إنشاء القيد المالي
        new_trans = WalletTransaction(
            wallet_id=wallet.id,
            trans_type=trans_type,
            source_type='voucher', # أو 'sale_revenue' حسب طبيعة الحركة
            amount=amount,
            currency=currency,
            reference_number=order_ref,      # سند التسوية
            related_order_id=order_ref,      # الربط المباشر برقم الطلب (قمره)
            balance_before=balance_before,
            balance_after=balance_after,
            description=f"عملية مالية للطلب رقم {order_ref}"
        )
        
        db.session.add(new_trans)
        db.session.commit()
        flash(f"تم تسجيل العملية للطلب {order_ref} بنجاح.", "success")
        
    except Exception as e:
        db.session.rollback()
        flash("حدث خطأ تقني أثناء معالجة السند.", "danger")

    return redirect(url_for('wallet_app.manage_wallet', supplier_id=supplier_id))
