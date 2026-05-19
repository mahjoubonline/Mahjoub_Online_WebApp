# coding: utf-8
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from apps import db
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import Wallet

admin_wallet = Blueprint('admin_wallet', __name__, template_folder='templates')

@admin_wallet.route('/admin/wallet/overview', methods=['GET'])
@login_required
def overview():
    wallets = Wallet.query.all()
    totals = {
        'total_yer': sum(w.yer_available or 0 for w in wallets),
        'total_sar': sum(w.sar_available or 0 for w in wallets),
        'total_usd': sum(w.usd_available or 0 for w in wallets)
    }
    return render_template('admin/overview.html', totals=totals)

@admin_wallet.route('/admin/wallet/search_api', methods=['GET'])
@login_required
def search_api():
    search_query = request.args.get('query', '').strip()
    filter_type = request.args.get('filter', 'none') # 'none' يعني إخفاء الجميع عند التحميل
    
    if filter_type == 'none':
        return jsonify({"wallets": []})

    query = db.session.query(Wallet, Supplier).outerjoin(Supplier, Wallet.supplier_id == Supplier.sovereign_id)
    
    if filter_type == 'active':
        query = query.filter((Wallet.yer_available > 0) | (Wallet.sar_available > 0) | (Wallet.usd_available > 0))
    elif filter_type == 'idle':
        query = query.filter((Wallet.yer_available <= 0) & (Wallet.sar_available <= 0) & (Wallet.usd_available <= 0))
        
    if search_query:
        query = query.filter((Supplier.trade_name.ilike(f'%{search_query}%')) | (Wallet.wallet_code.ilike(f'%{search_query}%')))
    
    results = [{"id": w.id, "wallet_code": w.wallet_code, "trade_name": s.trade_name if s else 'غير معرف', "sovereign_id": w.supplier_id, "yer_balance": float(w.yer_available or 0), "sar_balance": float(w.sar_available or 0), "usd_balance": float(w.usd_available or 0)} for w, s in query.all()]
    return jsonify({"wallets": results})

@admin_wallet.route('/admin/wallet/adjust', methods=['POST'])
@login_required
def adjust_balance():
    wallet_id = request.form.get('wallet_id')
    currency = request.form.get('currency')
    action_type = request.form.get('action_type')
    # إذا كانت سحب نثبت القيمة على 30، غير ذلك نأخذ المدخل
    amount = 30.0 if action_type == 'withdrawal' else float(request.form.get('amount', 0))
    
    wallet = Wallet.query.get(wallet_id)
    if wallet and amount > 0:
        if action_type == 'deposit':
            if currency == 'YER': wallet.yer_total += amount
            elif currency == 'SAR': wallet.sar_total += amount
            elif currency == 'USD': wallet.usd_total += amount
        else: # سحب
            if currency == 'YER': wallet.yer_withdrawn += amount
            elif currency == 'SAR': wallet.sar_withdrawn += amount
            elif currency == 'USD': wallet.usd_withdrawn += amount
        db.session.commit()
        flash(f'تم تنفيذ العملية بقيمة {amount}', 'success')
    return redirect(url_for('admin_wallet.overview'))
