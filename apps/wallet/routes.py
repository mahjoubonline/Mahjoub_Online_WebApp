# coding: utf-8
from flask import Blueprint, render_template, request, jsonify
from apps import db
# استيراد الموديلات بالأسماء الصحيحة (wallet_db و supplier_db)
from apps.models.wallet_db import SupplierWallet
from apps.models.supplier_db import Supplier
from sqlalchemy import or_

# تعريف الـ Blueprint
wallet_app = Blueprint('wallet_app', __name__, template_folder='templates')

# 1. لوحة التحكم الرئيسية للمحافظ
@wallet_app.route('/wallet', methods=['GET'])
def dashboard():
    search = request.args.get('search', '')
    # التأكد من استخدام اسم الموديل الصحيح SupplierWallet
    query = SupplierWallet.query.join(Supplier)
    
    if search:
        query = query.filter(or_(
            Supplier.trade_name.contains(search),
            Supplier.owner_phone.contains(search), # تأكد من اسم الحقل في موديل المورد
            SupplierWallet.id.contains(search)
        ))
    
    wallets = query.all()
    return render_template('admin/wallet_app.html', wallets=wallets)

# 2. البحث الذكي (Select2)
@wallet_app.route('/wallet/search_suppliers')
def search_suppliers():
    term = request.args.get('term', '')
    suppliers = Supplier.query.filter(
        or_(Supplier.trade_name.contains(term), Supplier.owner_phone.contains(term))
    ).limit(10).all()
    
    results = [{'id': s.id, 'text': f"{s.trade_name} - {s.owner_phone}"} for s in suppliers]
    return jsonify({'results': results})

# 3. جلب قائمة الموردين
@wallet_app.route('/wallet/get_suppliers_list')
def get_suppliers_list():
    page = request.args.get('page', 1, type=int)
    suppliers = Supplier.query.paginate(page=page, per_page=10)
    return render_template('admin/partials/suppliers_table.html', suppliers=suppliers)

# 4. عرض كشف حساب المورد
@wallet_app.route('/wallet/view/<int:supplier_id>')
def view_wallet(supplier_id):
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier_id).first_or_404()
    return render_template('admin/partials/wallet_details.html', wallet=wallet)

# 5. عرض تفاصيل المحفظة
@wallet_app.route('/wallet/manage/<int:supplier_id>')
def manage_wallet(supplier_id):
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier_id).first_or_404()
    return render_template('admin/view_wallet.html', wallet=wallet)
