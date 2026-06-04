# coding: utf-8
# 📂 apps/admin_dashboard/routes.py - لوحة التحكم السيادية

from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from apps.extensions import db
from sqlalchemy import func

# ✅ تعريف الـ Blueprint: يتم ربطه بـ '/admin' في __init__.py
admin_dashboard = Blueprint(
    'admin_dashboard', 
    __name__, 
    template_folder='templates'
)

@admin_dashboard.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    # التحقق من صلاحية الوصول (Owner أو Admin فقط)
    if current_user.role not in ['Owner', 'Admin']:
        abort(403)

    from apps.models.supplier_db import Supplier
    from apps.models.wallet_db import SupplierWallet, WalletTransaction
    from apps.models.statement_db import SupplierStatement

    try:
        # 📊 استخراج إحصائيات النظام (مثال)
        stats = {
            'total_suppliers': Supplier.query.count(),
            'total_balance': db.session.query(func.sum(SupplierWallet.balance)).scalar() or 0,
            'recent_transactions': WalletTransaction.query.order_by(WalletTransaction.id.desc()).limit(5).all()
        }
        
        # تقديم القالب: يبحث داخل apps/admin_dashboard/templates/admin/dashboard_content.html
        return render_template('admin/dashboard_content.html', **stats)
        
    except Exception as e:
        print(f"🚨 خطأ في تحميل الداشبورد: {e}")
        return "حدث خطأ فني في لوحة التحكم.", 500
