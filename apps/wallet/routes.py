# coding: utf-8
# 💳 محرك الحوكمة المالية والمسارات السيادية للمحافظ اللحظية - منصة محجوب أونلاين 2026

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from apps import db
from apps.models.supplier_db import Supplier

# 🛡️ استدعاء آمن ومحصن للموديلات لمنع الانهيار الكلي للسيرفر (Crash-Proof)
try:
    from apps.models.wallet_db import Wallet
except ImportError:
    class Wallet(object):
        query = None

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
    """ الشاشة الرئيسية لفحص وجرد الحسابات المادية """
    if current_user.role not in ['Owner', 'Admin']:
        flash('غير مسموح لك بامتلاك صلاحية دخول الفضاء المالي.', 'danger')
        return redirect(url_for('admin_dashboard.dashboard_home'))

    # جلب كافة المحافظ أولياً لعرضها في الجدول
    wallets = []
    if Wallet.query is not None:
        try:
            wallets = Wallet.query.join(Supplier, Wallet.supplier_id == Supplier.id).all()
        except Exception as e:
            print(f"📡 تنبيه حوكمة المحافظ: جاري مواءمة الجداول الهيكلية: {e}")

    return render_template('admin/overview.html', wallets=wallets)


@admin_wallet.route('/admin/wallet/search_api', methods=['GET'])
@login_required
def search_api():
    """ واجهة برمجية فورية (API) للبحث اللحظي وجلب بيانات المحافظ المحدثة """
    if current_user.role not in ['Owner', 'Admin']:
        return jsonify({"status": "error", "message": "صلاحية مرفوضة"}), 403

    search_query = request.args.get('query', '').strip()
    results = []

    if Wallet.query is None:
        return jsonify({"status": "success", "wallets": []})

    try:
        query = Wallet.query.join(Supplier, Wallet.supplier_id == Supplier.id)
        
        if search_query:
            query = query.filter(
                (Supplier.trade_name.like(f'%{search_query}%')) |
                (Supplier.sovereign_id.like(f'%{search_query}%')) |
                (Wallet.wallet_code.like(f'%{search_query}%'))
            )
        
        wallets = query.all()
        
        for w in wallets:
            results.append({
                "id": w.id,
                "wallet_code": w.wallet_code,
                "trade_name": w.supplier.trade_name if w.supplier else 'غير معرف',
                "sovereign_id": w.supplier.sovereign_id if w.supplier else '-',
                "yer_balance": float(getattr(w, 'yer_balance', 0.0)),
                "sar_balance": float(getattr(w, 'sar_balance', 0.0)),
                "usd_balance": float(getattr(w, 'usd_balance', 0.0))
            })
    except Exception as e:
        print(f"❌ خطأ أثناء البحث اللحظي: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify({"status": "success", "wallets": results})


@admin_wallet.route('/admin/wallet/adjust', methods=['POST'])
@login_required
def adjust_balance():
    """ سلطة الضبط المباشر للمالك لتعديل وحفظ الأرصدة الثلاثية """
    if current_user.role != 'Owner':
        flash('هذا الإجراء يتطلب سلطة المالك السيادية المطلقة.', 'danger')
        return redirect(url_for('admin_wallet.overview'))

    wallet_id = request.form.get('wallet_id')
    currency = request.form.get('currency')  
    action_type = request.form.get('action_type')  
    amount_str = request.form.get('amount', '0')

    try:
        amount = float(amount_str)
        if amount <= 0:
            flash('يجب أن تكون القيمة المالية أكبر من صفر.', 'warning')
            return redirect(url_for('admin_wallet.overview'))
            
        wallet = Wallet.query.get(wallet_id)
        if not wallet:
            flash('المحفظة المستهدفة غير مسجلة في الفضاء المالي.', 'danger')
            return redirect(url_for('admin_wallet.overview'))

        # منطق المعالجة المالية
        if currency == 'YER':
            current_bal = float(getattr(wallet, 'yer_balance', 0.0))
            wallet.yer_balance = (current_bal + amount) if action_type == 'deposit' else (current_bal - amount)
        elif currency == 'SAR':
            current_bal = float(getattr(wallet, 'sar_balance', 0.0))
            wallet.sar_balance = (current_bal + amount) if action_type == 'deposit' else (current_bal - amount)
        elif currency == 'USD':
            current_bal = float(getattr(wallet, 'usd_balance', 0.0))
            wallet.usd_balance = (current_bal + amount) if action_type == 'deposit' else (current_bal - amount)
        
        # توثيق العملية في سجل الحركات (Audit Log)
        if WalletTransaction is not None:
            tx_log = WalletTransaction(
                wallet_id=wallet.id,
                transaction_type=action_type,
                currency=currency,
                amount=amount,
                description=f"تعديل إداري من المالك: {action_type} بمبلغ {amount} {currency}"
            )
            db.session.add(tx_log)

        db.session.commit()
        flash(f'تم تنفيذ الفرمان المالي بنجاح على المحفظة {wallet.wallet_code}.', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'تعذر تنفيذ الفرمان المالي: {e}', 'danger')

    return redirect(url_for('admin_wallet.overview'))
