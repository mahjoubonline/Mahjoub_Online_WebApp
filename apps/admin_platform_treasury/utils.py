# coding: utf-8
# 📂 apps/admin_platform_treasury/utils.py

from datetime import datetime
from sqlalchemy import func
from apps.models.wallet_db import WalletTransaction, SupplierWallet
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
    إحصائيات الخزينة المحدثة بناءً على دفتر الأستاذ (القيد المزدوج).
    """
    # حساب إجمالي المدين (الخارج) والدائن (الداخل) لكل العملات
    stats = db_session.session.query(
        func.sum(WalletTransaction.credit).label('total_credit'),
        func.sum(WalletTransaction.debit).label('total_debit')
    ).filter(WalletTransaction.currency == 'SAR').first()
    
    # رصيد الخزينة الفعلي = إجمالي الدائن - إجمالي المدين
    credit = stats[0] or 0
    debit = stats[1] or 0
    net_balance = credit - debit
    
    return {
        'total_credit': credit,
        'total_debit': debit,
        'net_balance': net_balance,
        'total_sar': net_balance # المرجع الأساسي للخزينة
    }
