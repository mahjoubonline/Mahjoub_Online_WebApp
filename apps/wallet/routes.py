# coding: utf-8
# 📂 apps/wallet/routes.py - المحرك المالي للمحفظة

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import SupplierWallet, WalletTransaction

# تعريف التطبيق المستقل (Blueprint)
wallet_bp = Blueprint('wallet_app', __name__, template_folder='templates')

# 1. محرك البحث (يُستخدم في شريط البحث الذكي)
@wallet_bp.route('/api/search', methods=['GET'])
@login_required
def search_suppliers():
    query = request.args.get('q', '')
    if len(query) < 2: return jsonify([])
    
    # بحث سريع في الموردين
    suppliers = Supplier.query.filter(Supplier.name.ilike(f'%{query}%')).limit(10).all()
    return jsonify([{'id': s.id, 'name': s.name} for s in suppliers])

# 2. محرك استدعاء المحفظة (يُستخدم لعرض بيانات المورد في النافذة)
@wallet_bp.route('/view/<int:supplier_id>')
@login_required
def view_wallet(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier.id).first()
    
    # إذا لم توجد محفظة، ننشئ كائناً فارغاً
    if not wallet:
        wallet = type('obj', (object,), {'balance_sar': 0, 'balance_yer': 0, 'balance_usd': 0})
        transactions = []
    else:
        transactions = WalletTransaction.query.filter_by(wallet_id=wallet.id)\
            .order_by(WalletTransaction.created_at.desc()).limit(20).all()

    # هنا يتم استدعاء ملف الـ HTML "الرشيق" الذي صممناه
    return render_template('admin/wallet_app.html', 
                           supplier=supplier, 
                           wallet=wallet, 
                           transactions=transactions)
