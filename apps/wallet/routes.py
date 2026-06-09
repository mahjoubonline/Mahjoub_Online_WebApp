# 📂 apps/wallet/routes.py
from flask import Blueprint, render_template, request
from flask_login import login_required
from apps.models.wallet_db import SupplierWallet
from apps.models.supplier_db import Supplier

# تعريف الـ Blueprint مع تحديد مجلد القوالب المحلي
# Flask يبحث هنا داخل: apps/wallet/templates
wallet_app = Blueprint('wallet_app', __name__, template_folder='templates')

@wallet_app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """
    عرض لوحة تحكم محافظ الموردين مع إمكانية البحث
    """
    search_query = request.args.get('search', '')
    
    # استخدام join للربط مع جدول الموردين لضمان دقة البيانات
    query = SupplierWallet.query.join(Supplier, SupplierWallet.supplier_id == Supplier.id)
    
    # تطبيق فلتر البحث إذا وُجد نص في شريط البحث
    if search_query:
        search_filter = f"%{search_query}%"
        query = query.filter(
            Supplier.trade_name.ilike(search_filter) | 
            Supplier.owner_name.ilike(search_filter) |
            Supplier.owner_phone.ilike(search_filter)
        )
    
    # تنفيذ الاستعلام
    wallets = query.all()
    
    # سيبحث Flask في: apps/wallet/templates/admin/wallet_app.html
    return render_template('admin/wallet_app.html', wallets=wallets)

@wallet_app.route('/view/<int:supplier_id>', methods=['GET'])
@login_required
def view_wallet(supplier_id):
    """
    عرض تفاصيل محفظة مورد محدد
    """
    # جلب المحفظة المحددة أو إظهار خطأ 404 إذا لم توجد
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier_id).first_or_404()
    
    # سيبحث Flask في: apps/wallet/templates/admin/view_wallet.html
    return render_template('admin/view_wallet.html', wallet=wallet)
