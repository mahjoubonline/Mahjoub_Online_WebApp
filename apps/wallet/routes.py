# 📂 apps/wallet/routes.py - نظام المحافظ (مُحدث لدعم الترقيم)
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required
from sqlalchemy import func
from apps.extensions import db
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import SupplierWallet, WalletTransaction

# تعريف الـ Blueprint
wallet_app = Blueprint('wallet_app', __name__)

@wallet_app.route('/view/<int:supplier_id>')
@login_required
def view_wallet(supplier_id):
    # جلب بيانات المورد والمحفظة
    supplier = Supplier.query.get_or_404(supplier_id)
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier.id).first()
    
    # تحديد رقم الصفحة (الافتراضي هو الصفحة 1)
    page = request.args.get('page', 1, type=int)
    
    # جلب العمليات مع نظام الترقيم (20 عملية لكل صفحة)
    # نستخدم paginate بدلاً من limit لسهولة التنقل
    pagination = WalletTransaction.query.filter_by(wallet_id=wallet.id)\
        .order_by(WalletTransaction.created_at.desc())\
        .paginate(page=page, per_page=20, error_out=False)
    
    transactions = pagination.items
    
    # إرسال البيانات للواجهة
    return render_template('admin/wallet_app_detail.html', 
                           supplier=supplier, 
                           wallet=wallet, 
                           transactions=transactions,
                           pagination=pagination)

@wallet_app.route('/api/stats')
@login_required
def get_stats():
    # حساب إجمالي أرصدة النظام (اختياري حسب حاجتك في الواجهة)
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
