# 📂 apps/admin_dashboard/routes.py
from flask import Blueprint, render_template, abort, session
from flask_login import login_required, current_user
from apps.extensions import db
from sqlalchemy import func
from datetime import datetime

admin_dashboard = Blueprint(
    'admin_dashboard', 
    __name__, 
    template_folder='templates' # Flask سيبحث هنا تلقائياً عن مجلد 'admin'
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

    from apps.models.supplier_db import Supplier
    from apps.models.wallet_db import SupplierWallet, WalletTransaction

    try:
        stats = {
            'total_suppliers': Supplier.query.count(),
            'total_balance': db.session.query(func.sum(SupplierWallet.balance)).scalar() or 0,
            'recent_transactions': WalletTransaction.query.order_by(WalletTransaction.id.desc()).limit(5).all(),
            'now': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # التأكد من المسار النسبي داخل مجلد الـ templates
        return render_template('admin/dashboard_content.html', **stats)
        
    except Exception as e:
        return f"🚨 خطأ تقني في قاعدة البيانات: {str(e)}", 500
