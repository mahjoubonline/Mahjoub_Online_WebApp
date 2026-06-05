# coding: utf-8
# 📂 apps/wallet/routes.py - مسارات تطبيق المحفظة

from flask import Blueprint, render_template, abort
from flask_login import login_required
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import SupplierWallet, WalletTransaction

# تعريف التطبيق المستقل (Blueprint)
wallet_bp = Blueprint('wallet_app', __name__, template_folder='templates')

@wallet_bp.route('/view/<int:supplier_id>')
@login_required
def view_wallet(supplier_id):
    # 1. جلب بيانات المورد
    supplier = Supplier.query.get_or_404(supplier_id)
    
    # 2. جلب المحفظة المرتبطة بالمورد
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier.id).first()
    
    # إذا لم توجد محفظة (حالة نادرة)، ننشئ كائناً فارغاً لتجنب الأخطاء
    if not wallet:
        wallet = {'balance_sar': 0, 'balance_yer': 0, 'balance_usd': 0}
        transactions = []
    else:
        # 3. جلب سجل العمليات مرتباً من الأحدث للأقدم
        transactions = WalletTransaction.query.filter_by(wallet_id=wallet.id)\
            .order_by(WalletTransaction.created_at.desc()).limit(50).all()

    # إرجاع القالب كـ HTML جزئي ليتم عرضه في النافذة المنبثقة
    return render_template('admin/wallet_app.html', 
                           supplier=supplier, 
                           wallet=wallet, 
                           transactions=transactions)
