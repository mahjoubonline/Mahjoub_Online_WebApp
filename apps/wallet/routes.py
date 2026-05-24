# coding: utf-8
from flask import Blueprint, render_template, request
from flask_login import login_required
from apps import db
from apps.models import Wallet, Supplier
from apps.models.settlements_db import AdminSettlement

# قمت بتغيير الاسم هنا ليتطابق تماماً مع ما استوردته في __init__.py
wallet_blueprint = Blueprint('wallet', __name__)

@wallet_blueprint.route('/management', methods=['GET'])
@login_required
def display_management_table():
    search_query = request.args.get('search_query')
    wallet = None
    wallet_settlements = []
    
    # إحصائيات النظام العامة
    total_wallets_count = Wallet.query.count()
    total_yer_system = db.session.query(db.func.sum(Wallet.yer_available)).scalar() or 0
    total_sar_system = db.session.query(db.func.sum(Wallet.sar_available)).scalar() or 0
    
    if search_query:
        # البحث الشامل مع التأكد من وجود العلاقات في الموديلات
        wallet = Wallet.query.join(Supplier).filter(
            (Wallet.wallet_code.ilike(f'%{search_query}%')) |
            (Wallet.supplier_id.ilike(f'%{search_query}%')) |
            (Supplier.name.ilike(f'%{search_query}%')) |
            (Supplier.owner_name.ilike(f'%{search_query}%'))
        ).first()
        
        if wallet:
            # جلب التسويات المرتبطة بالمحفظة
            wallet_settlements = AdminSettlement.query.filter_by(
                wallet_id=wallet.id
            ).order_by(AdminSettlement.created_at.desc()).all()
    
    return render_template(
        'admin/settlement_and_withdrawal.html',
        wallet=wallet,
        wallet_settlements=wallet_settlements,
        total_wallets_count=total_wallets_count,
        total_yer_system=total_yer_system,
        total_sar_system=total_sar_system,
        current_search=search_query
    )
