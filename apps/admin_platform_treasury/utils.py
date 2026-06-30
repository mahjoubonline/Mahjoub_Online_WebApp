# coding: utf-8
# 📂 apps/admin_platform_treasury/utils.py

from datetime import datetime
from sqlalchemy import func
from apps.models.wallet_db import WalletTransaction, SupplierWallet
from apps.utils.time_utils import format_full_timestamp
from apps.extensions import db

def get_filtered_transactions(currency=None, start_date=None, end_date=None):
    """
    الدالة التي يتوقعها routes.py - تعيد Query جاهز للـ Pagination
    """
    query = WalletTransaction.query.order_by(WalletTransaction.created_at.desc())

    if currency and currency != 'all':
        query = query.filter(WalletTransaction.currency == currency)

    if start_date:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        query = query.filter(WalletTransaction.created_at >= start)
    
    if end_date:
        end = datetime.strptime(end_date, '%Y-%m-%d 23:59:59')
        query = query.filter(WalletTransaction.created_at <= end)

    return query

def get_treasury_stats(db_session):
    """
    إحصائيات الخزينة العامة.
    """
    stats = db_session.session.query(
        func.sum(SupplierWallet.balance_sar).label('total_sar'),
        func.sum(SupplierWallet.balance_usd).label('total_usd'),
        func.sum(SupplierWallet.balance_yer).label('total_yer')
    ).first()
    
    return {
        'total_sar': stats[0] or 0,
        'total_usd': stats[1] or 0,
        'total_yer': stats[2] or 0
    }
