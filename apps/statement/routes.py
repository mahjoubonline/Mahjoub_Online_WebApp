# coding: utf-8
from flask import render_template, request, jsonify
from flask_login import login_required
from apps.extensions import db
from apps.statement import statement_blueprint
from apps.models.supplier_db import Supplier
from apps.models.statement_db import SupplierStatement
from apps.models.wallet_db import SupplierWallet, WalletTransaction
from sqlalchemy import or_, func

@statement_blueprint.route('/view', methods=['GET'])
@login_required
def view_statement():
    currencies = ['USD', 'YER', 'SAR'] 
    return render_template('admin/statement.html', currencies=currencies)

# 1. البحث الذكي المتوافق مع متطلبات الـ Select2
@statement_blueprint.route('/api/suppliers/search', methods=['GET'])
@login_required
def api_search_suppliers():
    term = request.args.get('q', '')
    if not term:
        return jsonify({"results": []})

    suppliers = Supplier.query.filter(or_(
        Supplier.trade_name.ilike(f'%{term}%'),
        Supplier.sovereign_id.ilike(f'%{term}%'),
        Supplier.store_name.ilike(f'%{term}%'),
        Supplier.owner_name.ilike(f'%{term}%')
    )).limit(15).all()
    
    # تنسيق العرض الاحترافي للمستخدم في القائمة المنسدلة
    results = [
        {
            'id': s.id, 
            'text': f"{s.trade_name} | {s.store_name} (المالك: {s.owner_name}) - المعرف: {s.sovereign_id}"
        } for s in suppliers
    ]
    return jsonify({"results": results})

# 2. جلب كشف الحساب الشامل (تفصيلي + إجمالي الأرباح والحركات)
@statement_blueprint.route('/api/statement/report', methods=['GET'])
@login_required
def api_get_report():
    s_id = request.args.get('id')
    curr = request.args.get('currency', 'ALL')
    start = request.args.get('start')
    end = request.args.get('end')

    if not s_id:
        return jsonify({'error': 'يرجى تحديد المورد أولاً'}), 400

    supplier = Supplier.query.get(s_id)
    if not supplier: 
        return jsonify({'error': 'المورد غير موجود بالشرائح الحالية'}), 404

    # أ. جلب كشف الحساب التفصيلي من SupplierStatement
    stmt_query = SupplierStatement.query.filter_by(supplier_id=supplier.id)
    if curr != 'ALL': 
        stmt_query = stmt_query.filter_by(currency=curr)
    if start and end: 
        stmt_query = stmt_query.filter(SupplierStatement.created_at.between(start, end))
    
    # ترتيب الحركات تنازلياً لعرض الأحدث دائماً في أعلى الجدول للوحة الإدارة
    statements = stmt_query.order_by(SupplierStatement.created_at.desc()).all()

    # ب. جلب الأرباح من العمليات المالية للمحفظة 
    # تم تعديل الفلتر ليعتمد على supplier_id الرقمي الموحد لضمان سلامة الاستعلام
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier.id).first()
    total_profit = 0
    
    if wallet:
        pq = WalletTransaction.query.filter_by(wallet_id=wallet.id)
        if curr != 'ALL': 
            pq = pq.filter_by(currency=curr)
        if start and end: 
            pq = pq.filter(WalletTransaction.created_at.between(start, end))
        
        # جلب الإجمالي مباشرة من قاعدة البيانات لتوظيف موارد السيرفر بالشكل الأمثل
        total_profit = pq.with_entities(func.sum(WalletTransaction.profit_margin)).scalar() or 0

    return jsonify({
        'summary': {
            'total_debit': float(sum(s.debit for s in statements)),
            'total_credit': float(sum(s.credit for s in statements)),
            'net_balance': float(sum(s.credit for s in statements) - sum(s.debit for s in statements)),
            'total_profit': float(total_profit)
        },
        'details': [{
            'date': s.created_at.strftime('%Y-%m-%d %H:%M'),
            'desc': s.description or '---',
            'ref': s.reference_number or '---',
            'currency': s.currency,
            'debit': float(s.debit),
            'credit': float(s.credit),
            'balance': float(s.running_balance) # الاعتماد المباشر على الرصيد المحسوب سطر بسطر في الموديل
        } for s in statements]
    })
