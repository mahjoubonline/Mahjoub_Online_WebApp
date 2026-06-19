# coding: utf-8
# 📂 apps/admin_dashboard/routes.py - النسخة السيادية (نظيفة من الأخطاء)

from flask import Blueprint, render_template, abort, session
from flask_login import login_required, current_user
from apps.extensions import db
from datetime import datetime

# استيراد النماذج المالية والسيادية
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import SupplierWallet, WalletTransaction

admin_dashboard = Blueprint(
    'admin_dashboard', 
    __name__, 
    template_folder='templates'
)

@admin_dashboard.before_request
@login_required
def make_session_permanent():
    session.permanent = True
    session.modified = True 

@admin_dashboard.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    if current_user.role not in ['Owner', 'Admin']:
        abort(403)

    try:
        total_suppliers = Supplier.query.count()
        all_wallets = SupplierWallet.query.all()
        
        total_sar = 0.0
        total_yer = 0.0
        total_usd = 0.0
        
        for w in all_wallets:
            try:
                val_sar = float(w.balance_sar) if w.balance_sar is not None else 0.0
                val_yer = float(w.balance_yer) if w.balance_yer is not None else 0.0
                val_usd = float(w.balance_usd) if w.balance_usd is not None else 0.0
                total_sar += val_sar
                total_yer += val_yer
                total_usd += val_usd
            except (ValueError, TypeError, Exception):
                continue

        recent_transactions = WalletTransaction.query.order_by(WalletTransaction.created_at.desc()).limit(10).all()
        
        context = {
            'total_suppliers': total_suppliers,
            'total_balance_sar': total_sar,
            'total_balance_yer': total_yer,
            'total_balance_usd': total_usd,
            'recent_transactions': recent_transactions,
            'now': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'user_name': current_user.username,
            'store_name': 'محجوب أونلاين'
        }
        
        return render_template('admin/dashboard_content.html', **context)
        
    except Exception as e:
        print(f"🚨 Dashboard Error: {str(e)}")
        return f"🚨 عطل في المحرك المالي: {str(e)}", 500

@admin_dashboard.route('/system_logs', methods=['GET'])
@login_required
def system_logs():
    if current_user.role != 'Owner':
        abort(403)
    return "سجل الأحداث السيادي - قيد المراقبة"
