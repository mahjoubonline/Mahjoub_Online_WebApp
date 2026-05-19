# coding: utf-8
# 💳 محرك الحوكمة المالية والمسارات السيادية للمحافظ اللحظية - منصة محجوب أونلاين 2026

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from apps import db
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import Wallet

# 🛡️ استدعاء آمن للموديل
WalletTransaction = None
try:
    import apps.models.wallet_db as w_model
    if hasattr(w_model, 'WalletTransaction'):
        WalletTransaction = getattr(w_model, 'WalletTransaction')
    elif hasattr(w_model, 'WalletTransactions'):
        WalletTransaction = getattr(w_model, 'WalletTransactions')
except Exception:
    pass

admin_wallet = Blueprint('admin_wallet', __name__, template_folder='templates')

@admin_wallet.route('/admin/wallet/overview', methods=['GET'])
@login_required
def overview():
    if current_user.role not in ['Owner', 'Admin']:
        flash('غير مسموح لك بامتلاك صلاحية دخول الفضاء المالي.', 'danger')
        return redirect(url_for('admin_dashboard.dashboard_home'))

    # جلب جميع المحافظ
    wallets = Wallet.query.all()
    
    # حساب الإجماليات برمجياً
    totals = {
        'total_yer': sum(w.yer_available for w in wallets),
        'total_sar': sum(w.sar_available for w in wallets),
        'total_usd': sum(w.usd_available for w in wallets)
    }

    return render_template('admin/overview.html', wallets=wallets, totals=totals)

@admin_wallet.route('/admin/wallet/search_api', methods=['GET'])
@login_required
def search_api():
    if current_user.role not in ['Owner', 'Admin']:
        return jsonify({"status": "error", "message": "صلاحية مرفوضة"}), 403

    search_query = request.args.get('query', '').strip()
    results = []

    try:
        # البحث باستخدام الربط على المعرف السيادي
        query = db.session.query(Wallet).outerjoin(Supplier, Wallet.supplier_id == Supplier.sovereign_id)
        
        if search_query:
            query = query.filter(
                (Supplier.trade_name.like(f'%{search_query}%')) |
                (Supplier.sovereign_id.like(f'%{search_query}%')) |
                (Wallet.wallet_code.like(f'%{search_query}%'))
            )
        
        for w, s in query.all():
            results.append({
                "id": w.id,
                "wallet_code": w.wallet_code,
                "trade_name": s.trade_name if s else 'غير معرف',
                "sovereign_id": w.supplier_id,
                "yer_balance": float(w.yer_available),
                "sar_balance": float(w.sar_available),
                "usd_balance": float(w.usd_available)
            })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify({"status": "success", "wallets": results})

@admin_wallet.route('/admin/wallet/adjust', methods=['POST'])
@login_required
def adjust_balance():
    if current_user.role != 'Owner':
        flash('هذا الإجراء يتطلب سلطة المالك السيادية.', 'danger')
        return redirect(url_for('admin_wallet.overview'))

    wallet_id = request.form.get('wallet_id')
    currency = request.form.get('currency')  
    action_type = request.form.get('action_type')  
    try:
        amount = float(request.form.get('amount', 0))
    except ValueError:
        amount = 0

    if amount <= 0:
        flash('يجب إدخال مبلغ صحيح.', 'warning')
        return redirect(url_for('admin_wallet.overview'))

    try:
        wallet = Wallet.query.get(wallet_id)
        if not wallet:
            flash('المحفظة غير موجودة.', 'danger')
            return redirect(url_for('admin_wallet.overview'))

        # التعديل بناءً على الأعمدة الفعلية
        if currency == 'YER':
            if action_type == 'deposit': wallet.yer_total += amount
            else: wallet.yer_withdrawn += amount
        elif currency == 'SAR':
            if action_type == 'deposit': wallet.sar_total += amount
            else: wallet.sar_withdrawn += amount
        elif currency == 'USD':
            if action_type == 'deposit': wallet.usd_total += amount
            else: wallet.usd_withdrawn += amount
        
        if WalletTransaction:
            db.session.add(WalletTransaction(
                wallet_id=wallet.id,
                transaction_type=action_type,
                currency=currency,
                amount=amount,
                description=f"تعديل إداري سيادي: {action_type} بمبلغ {amount} {currency}"
            ))

        db.session.commit()
        flash('تم تنفيذ الفرمان المالي بنجاح.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'عطل في التنفيذ: {e}', 'danger')

    return redirect(url_for('admin_wallet.overview'))
