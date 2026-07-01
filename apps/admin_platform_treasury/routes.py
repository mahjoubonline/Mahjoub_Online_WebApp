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

@treasury_bp.route('/dashboard', methods=['GET'])
@login_required
def index():
    """عرض الأستاذ العام (كشف حساب المنصة) مع دعم الترقيم والعملات."""
    
    # 1. فلتر العملات والصفحات
    currency = request.args.get('currency', 'SAR')
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # 2. إجمالي رصيد الخزينة (الرصيد التراكمي لآخر حركة)
    last_trans = WalletTransaction.query.order_by(WalletTransaction.id.desc()).first()
    total_balance = last_trans.balance_after if last_trans else 0.00
    
    # 3. إجمالي محفظة الموردين
    total_supplier_wallet = db.session.query(func.sum(SupplierWallet.balance_sar)).scalar() or 0.00
    
    # 4. الترقيم (Pagination) للحركات المالية
    pagination = WalletTransaction.query.order_by(WalletTransaction.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # 5. معالجة البيانات للعرض
    processed_transactions = []
    for t in pagination.items:
        is_credit = t.trans_type in ['credit', 'adjustment_credit', 'sale_revenue']
        processed_transactions.append({
            'voucher_number': t.voucher_number,
            'created_at': t.created_at,
            'description': t.description,
            'related_order_id': getattr(t, 'related_order_id', None),
            'debit': 0.00 if is_credit else t.amount,
            'credit': t.amount if is_credit else 0.00,
            'balance_after': t.balance_after
        })

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
    """دالة البحث المتقدم عن سند معين"""
    voucher = request.args.get('voucher')
    if voucher:
        # البحث المباشر
        transactions = WalletTransaction.query.filter(
            WalletTransaction.voucher_number.like(f"%{voucher}%")
        ).all()
        # تحويل بسيط للعرض
        processed = []
        for t in transactions:
            is_credit = t.trans_type in ['credit', 'adjustment_credit', 'sale_revenue']
            processed.append({
                'voucher_number': t.voucher_number,
                'created_at': t.created_at,
                'description': t.description,
                'debit': 0.00 if is_credit else t.amount,
                'credit': t.amount if is_credit else 0.00,
                'balance_after': t.balance_after
            })
        return render_template('admin_platform_treasury.html', transactions=processed)
    return index()

def register_module(app):
    app.register_blueprint(treasury_bp, url_prefix='/admin/treasury')
