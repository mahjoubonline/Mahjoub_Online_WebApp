# coding: utf-8
from flask import render_template
from flask_login import login_required
from apps.statement import statement_blueprint
from apps.models.statement_db import SupplierStatement
from apps.models.supplier_db import Supplier

@statement_blueprint.route('/view', defaults={'supplier_id': None})
@statement_blueprint.route('/view/<int:supplier_id>')
@login_required
def view_statement(supplier_id):
    all_suppliers = Supplier.query.order_by(Supplier.trade_name.asc()).all()
    statements = []
    supplier = None
    # أرصدة العملات الصافية
    balances = {'SAR': 0.0, 'YER': 0.0, 'USD': 0.0}

    if supplier_id:
        supplier = Supplier.query.get_or_404(supplier_id)
        statements = SupplierStatement.query.filter_by(supplier_id=supplier_id)\
                                           .order_by(SupplierStatement.created_at.desc()).all()
        
        # حساب الأرصدة الفعلية لكل عملة بدون خصومات
        for stmt in statements:
            if stmt.currency in balances:
                balances[stmt.currency] += (float(stmt.credit or 0) - float(stmt.debit or 0))

    return render_template('admin/statement.html', 
                           statements=statements,
                           all_suppliers=all_suppliers,
                           selected_supplier=supplier,
                           balances=balances)
