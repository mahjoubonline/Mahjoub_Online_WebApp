# coding: utf-8
from flask import render_template, request, jsonify
from flask_login import login_required
from sqlalchemy import or_, func
from apps.statement import statement_blueprint
from apps.models.supplier_db import Supplier
from apps.models.statement_db import SupplierStatement
from apps.models.wallet_db import SupplierWallet, WalletTransaction

@statement_blueprint.route('/view', methods=['GET'])
@login_required
def view_statement():
    # 1. البحث عن المورد (إما عبر القائمة أو البحث النصي)
    search_query = request.args.get('q')
    supplier_id = request.args.get('supplier_id')
    
    selected_supplier = None
    statements = []
    wallet = None
    
    # 2. منطق البحث الذكي (متجر، مالك، ID)
    if search_query:
        selected_supplier = Supplier.query.filter(or_(
            Supplier.store_name.ilike(f'%{search_query}%'),
            Supplier.owner_name.ilike(f'%{search_query}%'),
            Supplier.sovereign_id == search_query
        )).first()
    elif supplier_id:
        selected_supplier = Supplier.query.get(supplier_id)

    # 3. جلب البيانات المالية في حال وجود المورد
    if selected_supplier:
        # جلب الكشوفات الخاصة به
        statements = SupplierStatement.query.filter_by(supplier_id=selected_supplier.id).order_by(SupplierStatement.created_at.desc()).all()
        # جلب المحفظة المرتبطة لبيانات العملات
        wallet = SupplierWallet.query.filter_by(supplier_id=selected_supplier.sovereign_id).first()

    return render_template(
        'admin/statement.html',
        selected_supplier=selected_supplier,
        statements=statements,
        wallet=wallet,
        search_query=search_query
    )

@statement_blueprint.route('/profit-report', methods=['GET'])
@login_required
def profit_report():
    """تقرير الأرباح التفصيلي للمنصة"""
    # حساب إجمالي الربح بالتجميع
    total_profit_yer = db.session.query(func.sum(WalletTransaction.profit_margin)).filter_by(currency='YER').scalar() or 0
    total_profit_sar = db.session.query(func.sum(WalletTransaction.profit_margin)).filter_by(currency='SAR').scalar() or 0
    total_profit_usd = db.session.query(func.sum(WalletTransaction.profit_margin)).filter_by(currency='USD').scalar() or 0
    
    recent_profits = WalletTransaction.query.order_by(WalletTransaction.created_at.desc()).limit(50).all()

    return render_template(
        'admin/profit_report.html',
        total_profit_yer=total_profit_yer,
        total_profit_sar=total_profit_sar,
        total_profit_usd=total_profit_usd,
        recent_profits=recent_profits
    )
