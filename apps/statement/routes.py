from flask import render_template, request
from flask_login import login_required
from apps.statement import statement_blueprint
from apps.models.statement_db import SupplierStatement
from apps.models.supplier_db import Supplier  # تأكد من استيراد نموذج الموردين

@statement_blueprint.route('/view', defaults={'supplier_id': None})
@statement_blueprint.route('/view/<int:supplier_id>')
@login_required
def view_statement(supplier_id):
    # 1. جلب قائمة جميع الموردين لعرضها في قائمة البحث
    all_suppliers = Supplier.query.all()
    
    statements = []
    supplier = None
    admin_profits = 0.0

    # 2. إذا تم اختيار مورد، نجلب حركاته
    if supplier_id:
        supplier = Supplier.query.get_or_404(supplier_id)
        # جلب الحركات بناءً على المورد
        statements = SupplierStatement.query.filter_by(supplier_id=supplier_id)\
                                           .order_by(SupplierStatement.created_at.desc()).all()
        
        # 3. منطق حساب أرباح الإدارة (مثال: يمكنك تعديله حسب نظامك)
        # هنا سنفترض أن الإدارة تأخذ نسبة أو مبلغاً من حركات هذا المورد
        admin_profits = sum([s.admin_fee for s in statements if hasattr(s, 'admin_fee')])

    return render_template('admin/statement.html', 
                           statements=statements,
                           all_suppliers=all_suppliers,
                           selected_supplier=supplier,
                           admin_profits=admin_profits)
