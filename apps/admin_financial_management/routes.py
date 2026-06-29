# coding: utf-8
# 📂 apps/admin_financial_management/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from apps.extensions import db
from apps.models.withdrawal_db import WithdrawalRequest
from apps.models.wallet_db import SupplierWallet, WalletTransaction
from datetime import datetime
from decimal import Decimal

admin_financial_bp = Blueprint('admin_financial', __name__, template_folder='templates')

@admin_financial_bp.route('/withdrawal-requests', methods=['GET'])
@login_required
def list_withdrawal_requests():
    """عرض طلبات السحب المعلقة للمسؤول المالي"""
    requests = WithdrawalRequest.query.filter_by(status='pending').order_by(WithdrawalRequest.requested_at.desc()).all()
    return render_template('admin_financial_management/admin_financial_management.html', requests=requests)

@admin_financial_bp.route('/process-withdrawal/<int:req_id>', methods=['POST'])
@login_required
def process_withdrawal(req_id):
    """معالجة طلب السحب (قبول أو رفض)"""
    req = WithdrawalRequest.query.get_or_404(req_id)
    action = request.form.get('action') # 'approve' أو 'reject'
    
    try:
        if action == 'approve':
            wallet = SupplierWallet.query.filter_by(supplier_id=req.supplier_id).first()
            
            # التحقق من وجود المحفظة وتوفر الرصيد
            if wallet and wallet.balance_sar >= req.amount:
                # 1. تحديث حالة الطلب
                req.status = 'completed'
                req.processed_at = datetime.utcnow()
                req.processed_by = current_user.id
                
                # 2. إنشاء حركة مالية (دفتر الأستاذ)
                balance_before = wallet.balance_sar
                balance_after = balance_before - req.amount
                
                transaction = WalletTransaction(
                    wallet_id=wallet.id,
                    trans_type='debit',
                    source_type='withdrawal',
                    amount=req.amount,
                    currency='SAR',
                    balance_before=balance_before,
                    balance_after=balance_after,
                    description=f"سحب رصيد - طلب رقم {req.id}",
                    reference_number=str(req.id),
                    created_by=current_user.id
                )
                
                # 3. تحديث رصيد المحفظة
                wallet.balance_sar = balance_after
                wallet.total_withdrawn = (wallet.total_withdrawn or 0) + req.amount
                
                db.session.add(transaction)
                db.session.commit()
                flash('تم قبول طلب السحب وتحديث المحفظة بنجاح.', 'success')
            else:
                flash('رصيد المحفظة غير كافٍ أو تعذر العثور على محفظة المورد.', 'danger')
                
        elif action == 'reject':
            req.status = 'rejected'
            req.admin_notes = request.form.get('notes')
            req.processed_at = datetime.utcnow()
            req.processed_by = current_user.id
            db.session.commit()
            flash('تم رفض طلب السحب بنجاح.', 'info')
            
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ أثناء معالجة الطلب: {str(e)}', 'danger')
        
    return redirect(url_for('admin_financial.list_withdrawal_requests'))
