# coding: utf-8
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from apps.extensions import db
from apps.models.wallet_db import SupplierWallet as Wallet, WalletTransaction
from apps.models.supplier_db import Supplier
from apps.models.settlements_db import AdminSettlement
from apps.models.statement_db import SupplierStatement

financial_blueprint = Blueprint('financial_ops', __name__, template_folder='templates')

@financial_blueprint.route('/withdrawal/handle/<int:tx_id>/<decision>', methods=['POST'])
@login_required
def handle_supplier_withdrawal(tx_id, decision):
    tx = WalletTransaction.query.get_or_404(tx_id)
    
    if decision == 'approve':
        ref_number = request.form.get('ref_number', 'N/A')
        financial_entity = request.form.get('financial_entity', 'N/A')
        
        new_settlement = AdminSettlement(
            wallet_id=tx.wallet_id,
            wallet_code=tx.wallet.wallet_code,
            settlement_code=AdminSettlement.generate_settlement_code(),
            settlement_type='سحب رصيد',
            currency='SAR',
            amount=tx.amount,
            reference_number=ref_number,
            financial_entity=financial_entity,
            reason_notes=f"تسوية سحب للمورد {tx.wallet.supplier.trade_name}",
            status='منفذة'
        )
        
        # الترحيل التلقائي للكشف (صافي المبلغ بدون عمولات)
        last_stmt = SupplierStatement.query.filter_by(supplier_id=tx.wallet.supplier.id)\
                                           .order_by(SupplierStatement.created_at.desc()).first()
        current_balance = last_stmt.running_balance if last_stmt else 0.0
        
        new_statement = SupplierStatement(
            supplier_id=tx.wallet.supplier.id,
            wallet_id=tx.wallet_id,
            description=f"سحب رصيد - مرجع: {ref_number}",
            currency='SAR',
            debit=tx.amount, 
            credit=0.00,
            running_balance=current_balance - tx.amount,
            reference_type='SETTLEMENT',
            reference_id=new_settlement.id
        )
        
        tx.status = 'ناجحة'
        db.session.add(new_settlement)
        db.session.add(new_statement)
        db.session.commit()
        
        return render_template('admin/settlement_notice.html', tx=tx, settlement=new_settlement)
    
    else:
        tx.status = 'مرفوضة'
        db.session.commit()
        return redirect(url_for('financial_ops.display_management_table', search_query=tx.wallet.wallet_code))
