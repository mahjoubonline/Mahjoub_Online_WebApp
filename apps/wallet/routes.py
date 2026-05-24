from flask import Blueprint, render_template, request, flash, redirect, url_for
from apps.models import db, Wallet, Settlement, WithdrawalRequest
# افترض أنك تستخدم Flask-Login للتحقق من الصلاحيات
from flask_login import login_required, current_user 

blueprint = Blueprint('wallet', __name__, url_prefix='/wallet')

@blueprint.route('/management', methods=['GET'])
@login_required
def display_management_table():
    search_query = request.args.get('search_query')
    wallet = None
    wallet_settlements = []
    
    # حساب الإحصائيات الشاملة للنظام
    total_wallets_count = Wallet.query.count()
    # هنا نقوم بجمع الأرصدة (يفضل عمل Aggregation في قاعدة البيانات لتحسين الأداء)
    total_yer_system = db.session.query(db.func.sum(Wallet.yer_available)).scalar() or 0
    total_sar_system = db.session.query(db.func.sum(Wallet.sar_available)).scalar() or 0
    total_usd_system = db.session.query(db.func.sum(Wallet.usd_available)).scalar() or 0
    
    if search_query:
        wallet = Wallet.query.filter(
            (Wallet.wallet_code == search_query) | 
            (Wallet.supplier_id == search_query)
        ).first()
        
        if wallet:
            wallet_settlements = Settlement.query.filter_by(wallet_id=wallet.id).order_by(Settlement.created_at.desc()).all()
    
    pending_withdrawals = WithdrawalRequest.query.filter_by(status='pending').all()
    
    return render_template('admin/wallet_management.html',
                           wallet=wallet,
                           wallet_settlements=wallet_settlements,
                           total_wallets_count=total_wallets_count,
                           total_yer_system=total_yer_system,
                           total_sar_system=total_sar_system,
                           total_usd_system=total_usd_system,
                           pending_withdrawals=pending_withdrawals,
                           current_search=search_query)

@blueprint.route('/settlement/execute/<wallet_code>', methods=['POST'])
@login_required
def execute_admin_settlement(wallet_code):
    wallet = Wallet.query.filter_by(wallet_code=wallet_code).first_or_404()
    
    # استلام البيانات من النموذج
    amount = float(request.form.get('amount'))
    st_type = request.form.get('settlement_type')
    currency = request.form.get('currency')
    reason = request.form.get('notes')
    
    # منطق التعديل على رصيد المحفظة
    if st_type == 'deposit':
        if currency == 'YER': wallet.yer_available += amount
        elif currency == 'SAR': wallet.sar_available += amount
        elif currency == 'USD': wallet.usd_available += amount
    else:
        # خصم
        if currency == 'YER': wallet.yer_available -= amount
        # ... إلخ
        
    # تسجيل عملية التسوية
    new_settlement = Settlement(
        wallet_id=wallet.id,
        amount=amount,
        settlement_type=st_type,
        currency=currency,
        reason_notes=reason,
        created_by=current_user.username,
        settlement_code=f"SETTLE-{wallet.wallet_code}-{db.session.query(Settlement).count() + 1}"
    )
    
    db.session.add(new_settlement)
    db.session.commit()
    
    flash("تم اعتماد قيد التسوية المالية بنجاح", "success")
    return redirect(url_for('wallet.display_management_table', search_query=wallet_code))

@blueprint.route('/withdrawal/handle/<int:tx_id>/<decision>', methods=['POST'])
@login_required
def handle_supplier_withdrawal(tx_id, decision):
    request_obj = WithdrawalRequest.query.get_or_404(tx_id)
    
    if decision == 'approve':
        request_obj.status = 'approved'
        # تنفيذ خصم فعلي من رصيد المحفظة المتاح هنا
    else:
        request_obj.status = 'rejected'
        
    db.session.commit()
    flash(f"تم {decision} طلب السحب بنجاح", "info")
    return redirect(url_for('wallet.display_management_table'))
