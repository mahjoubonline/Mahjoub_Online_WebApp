from flask import render_template
from flask_login import login_required
from apps.statement import statement_blueprint
from apps.models.statement_db import SupplierStatement

@statement_blueprint.route('/view/<int:wallet_id>')
@login_required
def view_statement(wallet_id):
    # جلب كشف الحساب الخاص بالمحفظة المطلوبة
    statements = SupplierStatement.query.filter_by(wallet_id=wallet_id)\
                                        .order_by(SupplierStatement.created_at.desc()).all()
    
    return render_template('admin/statement.html', statements=statements)
