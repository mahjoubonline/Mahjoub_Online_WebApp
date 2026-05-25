# coding: utf-8
from flask import render_template, request
from flask_login import login_required
from apps.statement import statement_blueprint
from apps.models.statement_db import SupplierStatement
from apps.models.supplier_db import Supplier

@statement_blueprint.route('/view', methods=['GET'])
@login_required
def view_statement():
    # استقبال معرف المورد من النموذج أو الرابط
    supplier_id = request.args.get('supplier_id')
    
    all_suppliers = Supplier.query.order_by(Supplier.trade_name.asc()).all()
    statements = []
    supplier = None
    balances = {'SAR': 0.0, 'YER': 0.0, 'USD': 0.0}

    if supplier_id:
        supplier = Supplier.query.get(supplier_id)
        if supplier:
            statements = SupplierStatement.query.filter_by(supplier_id=supplier_id)\
                                               .order_by(SupplierStatement.created_at.desc()).all()
            
            # حساب الأرصدة بدون عمولات
            for stmt in statements:
                if stmt.currency in balances:
                    credit = float(stmt.credit or 0)
                    debit = float(stmt.debit or 0)
                    balances[stmt.currency] += (credit - debit)

    return render_template('admin/statement.html', 
                           statements=statements,
                           all_suppliers=all_suppliers,
                           selected_supplier=supplier,
                           balances=balances)
