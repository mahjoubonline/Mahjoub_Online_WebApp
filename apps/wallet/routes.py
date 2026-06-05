# 📂 apps/wallet/routes.py - المحرك المالي الاحترافي
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from sqlalchemy import func
from apps.extensions import db
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import SupplierWallet, WalletTransaction

# تعريف المحرك (Blueprint)
wallet_app = Blueprint('wallet_app', __name__)

@wallet_app.route('/index')
@login_required
def index():
    """
    صفحة البحث الرئيسية للمحافظ (تظهر البطاقات العلوية وحقل البحث)
    """
    totals = db.session.query(
        func.sum(SupplierWallet.balance_sar),
        func.sum(SupplierWallet.balance_yer),
        func.sum(SupplierWallet.balance_usd)
    ).first()
    
    return render_template('admin/wallet_app.html', 
                           total_system_sar=float(totals[0] or 0),
                           total_system_yer=float(totals[1] or 0),
                           total_system_usd=float(totals[2] or 0))

@wallet_app.route('/view/<int:supplier_id>')
@login_required
def view_wallet(supplier_id):
    """
    عرض تفاصيل المحفظة الخاصة بمورد معين
    """
    supplier = Supplier.query.get_or_404(supplier_id)
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier.id).first()
    
    if not wallet:
        return "هذا المورد لا يمتلك محفظة حالياً.", 404

    page = request.args.get('page', 1, type=int)
    
    pagination = WalletTransaction.query.filter_by(wallet_id=wallet.id)\
        .order_by(WalletTransaction.created_at.desc())\
        .paginate(page=page, per_page=15, error_out=False)
    
    return render_template('admin/wallet_app_detail.html', 
                           supplier=supplier, 
                           wallet=wallet, 
                           transactions=pagination.items,
                           pagination=pagination)

@wallet_app.route('/stats')
@login_required
def get_stats():
    """
    إرجاع إحصائيات النظام المالية العامة بصيغة JSON
    """
    totals = db.session.query(
        func.sum(SupplierWallet.balance_sar),
        func.sum(SupplierWallet.balance_yer),
        func.sum(SupplierWallet.balance_usd)
    ).first()
    
    return jsonify({
        'sar': float(totals[0] or 0),
        'yer': float(totals[1] or 0),
        'usd': float(totals[2] or 0)
    })
