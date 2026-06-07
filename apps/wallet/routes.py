# 📂 apps/wallet/routes.py
from flask import render_template, request, jsonify
from flask_login import login_required
from sqlalchemy import func
from apps import db 

# استيراد الموديلات
from apps.models.wallet_db import SupplierWallet as Wallet, WalletTransaction as Transaction
from apps.models.supplier_db import Supplier

# استيراد الـ Blueprint
from apps.wallet import wallet_app

# 1. لوحة تحكم المحفظة (الداشبورد)
@wallet_app.route('/wallet_dashboard')
@login_required
def wallet_dashboard():
    # حساب الإحصائيات العامة للمحافظ
    stats = {
        "usd": db.session.query(func.sum(Wallet.balance_usd)).scalar() or 0,
        "sar": db.session.query(func.sum(Wallet.balance_sar)).scalar() or 0,
        "yer": db.session.query(func.sum(Wallet.balance_yer)).scalar() or 0,
        "count": Wallet.query.count()
    }
    return render_template('admin/wallet_app.html', stats=stats)

# 2. جلب قائمة الموردين مع التصفح (Pagination)
# هذا المسار يتم استدعاؤه عبر AJAX من صفحة wallet_app.html
@wallet_app.route('/get_suppliers_list')
@login_required
def get_suppliers_list():
    page = request.args.get('page', 1, type=int)
    # جلب 10 موردين في كل صفحة
    suppliers = Supplier.query.paginate(page=page, per_page=10, error_out=False)
    return render_template('admin/suppliers_list.html', suppliers=suppliers)

# ملاحظة: تم حذف دالة search_api من هنا لأنها موجودة في ملف apps/api/search.py
# لضمان عدم وجود تضارب في الـ Routing.

# 3. عرض محفظة مورد معين (يُستدعى عبر AJAX)
@wallet_app.route('/view/<int:supplier_id>')
@login_required
def view_wallet(supplier_id):
    page = request.args.get('page', 1, type=int)
    # جلب المحفظة المرتبطة بالمورد
    wallet = Wallet.query.filter_by(supplier_id=supplier_id).first_or_404()
    
    # جلب العمليات المالية لهذا المورد بترتيب تنازلي (الأحدث أولاً)
    transactions = Transaction.query.filter_by(wallet_id=wallet.id)\
        .order_by(Transaction.created_at.desc())\
        .paginate(page=page, per_page=10, error_out=False)
        
    return render_template('admin/view_wallet.html', wallet=wallet, transactions=transactions)
