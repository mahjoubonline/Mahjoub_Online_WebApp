# 📂 apps/admin_dashboard/routes.py

from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from apps.extensions import db
from apps.models import Supplier, SupplierWallet, WalletTransaction
from sqlalchemy import func

# 1. تعديل اسم الـ Blueprint ليصبح admin_dashboard_bp
admin_dashboard_bp = Blueprint(
    'admin_dashboard_bp', 
    __name__, 
    template_folder='templates'
)

# 2. تعديل اسم الدالة المرتبطة بالـ Blueprint
@admin_dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    # ... (باقي كود الدالة كما هو تماماً) ...
    try:
        totals = db.session.query(
            func.sum(SupplierWallet.balance_sar).label('total_sar'),
            func.sum(SupplierWallet.balance_yer).label('total_yer'),
            func.sum(SupplierWallet.balance_usd).label('total_usd')
        ).first()
        
        supplier_count = db.session.query(func.count(Supplier.id)).scalar()
        
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

    except Exception as e:
        print(f"❌ [Dashboard Error]: {str(e)}")
        flash("حدث خطأ أثناء تحميل بيانات لوحة التحكم.", "danger")
        return render_template('admin/dashboard.html', 
                               total_suppliers=0, 
                               total_balance_sar=0.0, 
                               total_balance_yer=0.0, 
                               total_balance_usd=0.0, 
                               recent_transactions=[])
