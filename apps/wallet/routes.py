# coding: utf-8
from flask import Blueprint, render_template, request, jsonify
from apps import db
from apps.models.wallet_db import SupplierWallet
from apps.models.supplier_db import Supplier
from sqlalchemy import or_
from flask_paginate import Pagination, get_page_parameter

# تعريف الـ Blueprint
wallet_app = Blueprint('wallet_app', __name__, template_folder='templates')

# 1. لوحة التحكم الرئيسية للمحافظ مع الترقيم (15 في الصفحة)
@wallet_app.route('/wallet', methods=['GET'])
def dashboard():
    # إعدادات الترقيم
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 15
    search = request.args.get('search', '')
    
    # بناء الاستعلام
    query = SupplierWallet.query.join(Supplier)
    
    if search:
        query = query.filter(or_(
            Supplier.trade_name.contains(search),
            Supplier.owner_phone.contains(search),
            SupplierWallet.id.contains(search)
        ))
    
    # جلب البيانات المحددة للصفحة الحالية
    total = query.count()
    wallets = query.offset((page - 1) * per_page).limit(per_page).all()
    
    # تهيئة كائن الترقيم
    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap5')
    
    return render_template('admin/wallet_app.html', wallets=wallets, pagination=pagination)

# 2. البحث الذكي (Select2)
@wallet_app.route('/wallet/search_suppliers')
def search_suppliers():
    term = request.args.get('term', '')
    suppliers = Supplier.query.filter(
        or_(Supplier.trade_name.contains(term), Supplier.owner_phone.contains(term))
    ).limit(10).all()
    
    results = [{'id': s.id, 'text': f"{s.trade_name} - {s.owner_phone}"} for s in suppliers]
    return jsonify({'results': results})

# 3. جلب قائمة الموردين (بقي كما هو لخدمة الـ Partials)
@wallet_app.route('/wallet/get_suppliers_list')
def get_suppliers_list():
    page = request.args.get('page', 1, type=int)
    suppliers = Supplier.query.paginate(page=page, per_page=15) # تم تعديله لـ 15
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
