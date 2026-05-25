# coding: utf-8
# 📂 apps/statement/routes.py
from flask import render_template, request, jsonify
from flask_login import login_required
from apps.statement import statement_blueprint
from apps.extensions import db
from sqlalchemy import or_

# 1. عرض الصفحة الرئيسية للكشوفات
@statement_blueprint.route('/view', methods=['GET'])
@login_required
def view_statement():
    return render_template('admin/statement.html')

# 2. مسار البحث الديناميكي عن الموردين (API للـ Select2)
@statement_blueprint.route('/admin/suppliers/search', methods=['GET'])
@login_required
def search_suppliers_api():
    from apps.models.supplier_db import Supplier
    term = request.args.get('term', '')
    
    # البحث في الاسم أو الرقم الموحد
    suppliers = Supplier.query.filter(or_(
        Supplier.trade_name.ilike(f'%{term}%'),
        Supplier.sovereign_id.ilike(f'%{term}%')
    )).limit(10).all()
    
    return jsonify([
        {'id': s.id, 'text': f"{s.trade_name} | {s.sovereign_id}"} 
        for s in suppliers
    ])

# 3. مسار جلب بيانات كشف الحساب لحظياً (API للجدول)
@statement_blueprint.route('/statement/get_data', methods=['GET'])
@login_required
def get_statement_data():
    from apps.models.statement_db import SupplierStatement
    
    supplier_id = request.args.get('id')
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    
    query = SupplierStatement.query.filter_by(supplier_id=supplier_id)
    
    if start_date:
        query = query.filter(SupplierStatement.created_at >= start_date)
    if end_date:
        query = query.filter(SupplierStatement.created_at <= end_date)
        
    statements = query.order_by(SupplierStatement.created_at.asc()).all()
    
    # تحويل البيانات إلى تنسيق JSON للجدول
    data = [stmt.to_dict() for stmt in statements]
    
    # حساب الإجماليات (للوحة المؤشرات)
    total_debit = sum(s.debit for s in statements)
    total_credit = sum(s.credit for s in statements)
    
    return jsonify({
        'statements': data,
        'summary': {
            'debit': total_debit,
            'credit': total_credit,
            'balance': total_credit - total_debit
        }
    })
