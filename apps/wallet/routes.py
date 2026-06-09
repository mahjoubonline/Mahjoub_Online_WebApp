# 📂 apps/wallet/routes.py
from flask import Blueprint, render_template, request
from flask_login import login_required
from apps.models.wallet_db import SupplierWallet, WalletTransaction
from apps.models.supplier_db import Supplier

# إعداد الـ Blueprint بدون تحديد template_folder داخلي، 
# ليعتمد Flask على المجلد العام للقوالب (apps/templates/)
wallet_app = Blueprint('wallet_app', __name__)

@wallet_app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    # 1. استقبال نص البحث من القالب
    search_query = request.args.get('search', '')
    
    # 2. جلب البيانات باستخدام join لضمان وجود المورد المرتبط بالمحفظة
    query = SupplierWallet.query.join(Supplier, SupplierWallet.supplier_id == Supplier.id)
    
    # 3. تطبيق فلتر البحث إذا وُجد
    if search_query:
        search_filter = f"%{search_query}%"
        query = query.filter(
            Supplier.trade_name.ilike(search_filter) | 
            Supplier.owner_name.ilike(search_filter) |
            Supplier.owner_phone.ilike(search_filter)
        )
    
    # 4. تنفيذ الاستعلام
    wallets = query.all()
    
    # 5. إرسال البيانات للقالب
    # Flask سيبحث الآن في المجلد الرئيسي: apps/templates/admin/wallet_app.html
    return render_template('admin/wallet_app.html', wallets=wallets)

@wallet_app.route('/view/<int:supplier_id>')
@login_required
def view_wallet(supplier_id):
    # جلب المحفظة الخاصة بالمورد المحدد
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier_id).first_or_404()
    
    # سيبحث Flask في: apps/templates/admin/view_wallet.html
    return render_template('admin/view_wallet.html', wallet=wallet)
