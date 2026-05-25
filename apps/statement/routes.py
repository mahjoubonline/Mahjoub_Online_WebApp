# coding: utf-8
from flask import render_template, request
from flask_login import login_required
from apps.statement import statement_blueprint
from apps.models.statement_db import SupplierStatement
from apps.models.supplier_db import Supplier
from sqlalchemy import func

@statement_blueprint.route('/view', defaults={'supplier_id': None})
@statement_blueprint.route('/view/<int:supplier_id>')
@login_required
def view_statement(supplier_id):
    # 1. جلب قائمة جميع الموردين لعرضها في قائمة البحث
    all_suppliers = Supplier.query.order_by(Supplier.trade_name.asc()).all()
    
    # 2. حساب إجمالي أرباح الإدارة من كل العمليات (لجميع الموردين)
    # نستخدم func.sum ليكون الحساب مباشراً من قاعدة البيانات (أسرع وأدق)
    total_admin_profits = db.session.query(func.sum(SupplierStatement.admin_fee)).scalar() or 0.0
    
    statements = []
    supplier = None
    admin_profits = 0.0

    # 3. إذا تم اختيار مورد، نجلب حركاته وتفاصيله
    if supplier_id:
        supplier = Supplier.query.get_or_404(supplier_id)
        
        # جلب الحركات الخاصة بهذا المورد فقط
        statements = SupplierStatement.query.filter_by(supplier_id=supplier_id)\
                                           .order_by(SupplierStatement.created_at.desc()).all()
        
        # حساب أرباح الإدارة الخاصة بهذا المورد المختار
        admin_profits = sum([s.admin_fee for s in statements if s.admin_fee is not None])

    return render_template('admin/statement.html', 
                           statements=statements,
                           all_suppliers=all_suppliers,
                           selected_supplier=supplier,
                           admin_profits=admin_profits,
                           total_admin_profits=total_admin_profits)
