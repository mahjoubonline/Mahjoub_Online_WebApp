# coding: utf-8
# 📂 apps/supplier_wallet/routes.py

from flask import Blueprint, render_template, abort, request
from flask_login import login_required, current_user
from flask_paginate import Pagination, get_page_parameter
from apps.models.wallet_db import SupplierWallet, WalletTransaction
from apps.api.sync_engine import SyncEngine
from datetime import datetime, timedelta
from sqlalchemy import func

supplier_wallet_bp = Blueprint('supplier_wallet', __name__, template_folder='templates')

@supplier_wallet_bp.route('/my-wallet', methods=['GET'])
@login_required
def view_my_wallet():
    # 1. جلب محفظة المورد
    wallet = SupplierWallet.query.filter_by(supplier_id=current_user.id).first()
    if not wallet:
        abort(404, description="لم يتم العثور على محفظة مرتبطة بحسابك.")

    # 2. الفلاتر الأساسية
    currency = request.args.get('currency', 'SAR')
    filter_type = request.args.get('filter_type', 'all')
    search = request.args.get('search', '').strip()
    
    query = WalletTransaction.query.filter_by(wallet_id=wallet.id, currency=currency)

    # 3. الفلترة الزمنية
    if filter_type == 'day':
        query = query.filter(WalletTransaction.created_at >= datetime.utcnow().date())
    elif filter_type == 'week':
        query = query.filter(WalletTransaction.created_at >= (datetime.utcnow() - timedelta(days=7)))
    elif filter_type == 'month':
        query = query.filter(WalletTransaction.created_at >= (datetime.utcnow() - timedelta(days=30)))
    
    # فلترة بالتاريخ المخصص
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if start_date: query = query.filter(WalletTransaction.created_at >= start_date)
    if end_date: query = query.filter(WalletTransaction.created_at <= end_date)

    # 4. البحث المرن
    if search:
        query = query.filter(
            (WalletTransaction.voucher_number.ilike(f'%{search}%')) | 
            (WalletTransaction.description.ilike(f'%{search}%'))
        )

    # 5. حساب الإجماليات (لكل الفترة المفلترة)
    # نستخدم func.sum للحصول على دقة عالية وسرعة من قاعدة البيانات مباشرة
    stats = query.with_entities(
        func.sum(WalletTransaction.amount).filter(WalletTransaction.trans_type.in_(['sale_revenue', 'adjustment_credit'])).label('total_credit'),
        func.sum(WalletTransaction.amount).filter(WalletTransaction.trans_type.in_(['withdrawal', 'adjustment_debit'])).label('total_debit')
    ).first()
    
    total_credit = stats.total_credit or 0
    total_debit = stats.total_debit or 0

    # 6. الترقيم (Pagination)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 20
    pagination = Pagination(page=page, total=query.count(), per_page=per_page, css_framework='bootstrap5')
    
    transactions = query.order_by(WalletTransaction.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()

    # 7. استجابة الـ AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('supplier_wallet/_table_partial.html', 
                               transactions=transactions, total_debit=total_debit, total_credit=total_credit)

    return render_template('supplier_wallet/supplier_wallet.html', 
                           wallet=wallet, transactions=transactions, pagination=pagination,
                           total_debit=total_debit, total_credit=total_credit)

@supplier_wallet_bp.route('/test-sync', methods=['GET'])
@login_required
def test_sync():
    if not current_user.is_admin: abort(403)
    if SyncEngine.fetch_and_sync_order():
        return "✅ تم تنفيذ المزامنة."
    return "❌ فشل المزامنة."
