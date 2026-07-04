# coding: utf-8
# 📂 apps/admin_platform_treasury/routes.py

from flask import Blueprint, render_template, request
from flask_login import login_required
from apps.extensions import db
from apps.models import WalletTransaction, SupplierWallet
from sqlalchemy import func

# تعريف البلوبرنت
treasury_bp = Blueprint(
    'treasury_bp', 
    __name__, 
    template_folder='templates'
)

def _process_transaction(t):
    """دالة مساعدة لمعالجة بيانات المعاملة الواحدة (لتجنب التكرار)."""
    is_credit = t.trans_type in ['credit', 'adjustment_credit', 'sale_revenue']
    return {
        'voucher_number': t.voucher_number,
        'created_at': t.created_at,
        'description': t.description,
        'related_order_id': getattr(t, 'related_order_id', None),
        'debit': 0.00 if is_credit else t.amount,
        'credit': t.amount if is_credit else 0.00,
        'balance_after': t.balance_after
    }

@treasury_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """عرض الأستاذ العام (كشف حساب المنصة)."""
    currency = request.args.get('currency', 'SAR')
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    base_query = WalletTransaction.query.filter_by(currency=currency)
    
    # الحصول على الرصيد الحالي
    last_trans = base_query.order_by(WalletTransaction.id.desc()).first()
    total_balance = last_trans.balance_after if last_trans else 0.00
    
    # حساب إجمالي محافظ الموردين
    try:
        total_supplier_wallet = db.session.query(func.sum(SupplierWallet.balance_sar)).scalar() or 0.00
    except Exception:
        total_supplier_wallet = 0.00
    
    # التقسيم (Pagination)
    pagination = base_query.order_by(WalletTransaction.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # معالجة البيانات باستخدام الدالة المساعدة
    processed_transactions = [_process_transaction(t) for t in pagination.items]

    return render_template(
        'admin_platform_treasury.html',
        transactions=processed_transactions,
        total_balance=total_balance,
        total_supplier_wallet=total_supplier_wallet,
        pagination=pagination,
        active_currency=currency
    )

@treasury_bp.route('/filter', methods=['GET'])
@login_required
def filter_treasury():
    """البحث المتقدم عن سند معين."""
    voucher = request.args.get('voucher')
    currency = request.args.get('currency', 'SAR')
    
    if voucher:
        transactions = WalletTransaction.query.filter(
            WalletTransaction.voucher_number.like(f"%{voucher}%"),
            WalletTransaction.currency == currency
        ).order_by(WalletTransaction.created_at.desc()).all()
        
        # معالجة البيانات باستخدام نفس الدالة المساعدة
        processed = [_process_transaction(t) for t in transactions]
        
        return render_template(
            'admin_platform_treasury.html', 
            transactions=processed, 
            active_currency=currency
        )
    return dashboard()
