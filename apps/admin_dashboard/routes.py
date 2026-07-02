# 📂 apps/admin_dashboard/routes.py

from flask import Blueprint, render_template, session, abort
from flask_login import login_required, current_user
# تأكد من استيراد النماذج (Models) اللازمة لحساب البيانات
from apps.models.wallet_db import SupplierWallet, WalletTransaction
from apps.models.supplier_db import Supplier 
from sqlalchemy import func

# ... (تعريف الـ Blueprint و admin_required كما هما) ...

@admin_dashboard.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    admin_required()
    
    # 1. حساب الإحصائيات الحقيقية من قاعدة البيانات
    total_suppliers = Supplier.query.count()
    
    # حساب الأرصدة المجمعة
    stats = db.session.query(
        func.sum(SupplierWallet.balance_sar),
        func.sum(SupplierWallet.balance_yer),
        func.sum(SupplierWallet.balance_usd)
    ).first()
    
    # 2. جلب آخر 10 عمليات مالية
    recent_transactions = WalletTransaction.query.order_by(
        WalletTransaction.created_at.desc()
    ).limit(10).all()
    
    # 3. إرسال البيانات للقالب
    context = {
        'total_suppliers': total_suppliers,
        'total_balance_sar': stats[0] or 0.00,
        'total_balance_yer': stats[1] or 0.00,
        'total_balance_usd': stats[2] or 0.00,
        'recent_transactions': recent_transactions
    }
    
    return render_template('admin/dashboard.html', **context)
