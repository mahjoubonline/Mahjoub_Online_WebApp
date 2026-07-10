# coding: utf-8
# 📂 apps/admin_dashboard/routes.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from apps.extensions import db
from apps.models import Supplier, SupplierWallet, WalletTransaction
from sqlalchemy import func

# 1. إنشاء الـ Blueprint
admin_dashboard = Blueprint(
    'admin_dashboard', 
    __name__, 
    template_folder='templates'
)

# 2. مسار لوحة التحكم
@admin_dashboard.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """عرض لوحة تحكم النظام الرئيسية مع الأرصدة المجمعة."""
    
    # جلب إجمالي الأرصدة من المحافظ باستخدام دوال التجميع لسرعة الأداء
    totals = db.session.query(
        func.sum(SupplierWallet.balance_sar).label('total_sar'),
        func.sum(SupplierWallet.balance_yer).label('total_yer'),
        func.sum(SupplierWallet.balance_usd).label('total_usd')
    ).first()
    
    # جلب عدد الموردين
    supplier_count = db.session.query(func.count(Supplier.id)).scalar()
    
    # جلب آخر 10 معاملات مالية
    recent_transactions = WalletTransaction.query.order_by(
        WalletTransaction.created_at.desc()
    ).limit(10).all()

    context = {
        "total_suppliers": supplier_count or 0,
        "total_balance_sar": float(totals.total_sar or 0),
        "total_balance_yer": float(totals.total_yer or 0),
        "total_balance_usd": float(totals.total_usd or 0),
        "recent_transactions": recent_transactions
    }
    
    return render_template('admin/dashboard.html', **context)
