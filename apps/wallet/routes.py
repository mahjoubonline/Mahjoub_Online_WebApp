# 📂 apps/wallet/routes.py
from flask import render_template, request, jsonify
from flask_login import login_required
from sqlalchemy import func, or_
from apps import db 
from apps.models.wallet_db import SupplierWallet as Wallet, WalletTransaction as Transaction
from apps.models.supplier_db import Supplier
from apps.wallet import wallet_app

# 1. مسار الداشبورد الرئيسي: يعرض القالب الأساسي مع الإحصائيات
@wallet_app.route('/wallet_dashboard')
@login_required
def wallet_dashboard():
    stats = {
        "usd": db.session.query(func.sum(Wallet.balance_usd)).scalar() or 0,
        "sar": db.session.query(func.sum(Wallet.balance_sar)).scalar() or 0,
        "yer": db.session.query(func.sum(Wallet.balance_yer)).scalar() or 0,
        "count": Wallet.query.count()
    }
    return render_template('admin/wallet_app.html', stats=stats)

# 2. مسار البحث الذكي (يخدم Select2 في القالب)
@wallet_app.route('/search_suppliers')
@login_required
def search_suppliers():
    query = request.args.get('q', '')
    suppliers = Supplier.query.filter(
        or_(
            Supplier.trade_name.contains(query),
            Supplier.owner_phone.contains(query)
        )
    ).limit(10).all()
    
    results = [{"id": s.id, "text": f"{s.trade_name} - {s.owner_phone}"} for s in suppliers]
    return jsonify({"results": results})

# 3. محرك جلب قائمة الموردين (يغذي الجدول داخل القالب)
@wallet_app.route('/get_suppliers_list')
@login_required
def get_suppliers_list():
    page = request.args.get('page', 1, type=int)
    suppliers = Supplier.query.paginate(page=page, per_page=10, error_out=False)
    # ملاحظة: suppliers_list.html يجب أن يحتوي على كود الجدول فقط (بدون extends)
    return render_template('admin/suppliers_list.html', suppliers=suppliers)

# 4. محرك عرض كشف المحفظة (يغذي منطقة العرض عند اختيار مورد)
@wallet_app.route('/view/<int:supplier_id>')
@login_required
def view_wallet(supplier_id):
    wallet = Wallet.query.filter_by(supplier_id=supplier_id).first_or_404()
    transactions = Transaction.query.filter_by(wallet_id=wallet.id)\
        .order_by(Transaction.created_at.desc())\
        .paginate(page=1, per_page=10, error_out=False)
    # ملاحظة: view_wallet.html يجب أن يحتوي على محتوى الكشف فقط (بدون extends)
    return render_template('admin/view_wallet.html', wallet=wallet, transactions=transactions)
