# coding: utf-8
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required
from apps import db 
from apps.models.wallet_db import SupplierWallet
from apps.models.supplier_db import Supplier
from sqlalchemy import func

# تعريف البلوبرينت باسم 'wallet'
wallet_bp = Blueprint('wallet', __name__, template_folder='templates')

@wallet_bp.route('/wallet_page')
@login_required
def wallet_home():
    """
    اسم الدالة هنا wallet_home يطابق ما يطلبه url_for في القوالب
    """
    totals = db.session.query(
        func.sum(SupplierWallet.yer_total).label('total_yer'),
        func.sum(SupplierWallet.sar_total).label('total_sar'),
        func.sum(SupplierWallet.usd_total).label('total_usd')
    ).first()
    
    totals_dict = {
        'total_yer': totals.total_yer or 0,
        'total_sar': totals.total_sar or 0,
        'total_usd': totals.total_usd or 0
    }
    
    return render_template('admin/wallet_dashboard.html', totals=totals_dict)

@wallet_bp.route('/adjust', methods=['POST'])
@login_required
def adjust_balance():
    wallet_id = request.form.get('wallet_id')
    currency = request.form.get('currency')
    amount = float(request.form.get('amount', 0))
    wallet = SupplierWallet.query.get_or_404(wallet_id)
    
    # ... (بقية كود التعديل) ...
    db.session.commit()
    # استخدام المسار المصحح
    return redirect(url_for('wallet.wallet_home'))
