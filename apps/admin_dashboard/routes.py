# coding: utf-8
# 📂 apps/admin_dashboard/routes.py - لوحة التحكم السيادية (مُصحح)

from flask import Blueprint, render_template, abort, session
from flask_login import login_required, current_user
from apps.extensions import db
from sqlalchemy import func
from datetime import datetime

admin_dashboard = Blueprint(
    'admin_dashboard', 
    __name__, 
    template_folder='templates'
)

@admin_dashboard.before_request
@login_required
def make_session_permanent():
    # تفعيل خمول الجلسة (15 دقيقة)
    session.permanent = True
    session.modified = True 

@admin_dashboard.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    # 🛡️ حماية سيادية
    if current_user.role not in ['Owner', 'Admin']:
        abort(403)

    from apps.models.supplier_db import Supplier
    from apps.models.wallet_db import SupplierWallet, WalletTransaction

    try:
        # استخراج الإحصائيات باستخدام الأعمدة الصحيحة من SupplierWallet
        total_sar = db.session.query(func.sum(SupplierWallet.sar_total)).scalar() or 0
        total_yer = db.session.query(func.sum(SupplierWallet.yer_total)).scalar() or 0
        
        stats = {
            'total_suppliers': Supplier.query.count(),
            'total_balance_sar': total_sar,
            'total_balance_yer': total_yer,
            'recent_transactions': WalletTransaction.query.order_by(WalletTransaction.id.desc()).limit(5).all(),
            'now': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # تقديم القالب
        return render_template('admin/dashboard_content.html', **stats)
        
    except Exception as e:
        # 🔐 إظهار تفاصيل الخطأ مؤقتاً للتصحيح، ويمكنك إخفاؤها لاحقاً
        return f"🚨 خطأ تقني في قاعدة البيانات: {str(e)}", 500
