# coding: utf-8
# 📂 apps/wallet/routes.py

from flask import Blueprint, render_template, request, jsonify, abort
# تم تصحيح الاستيراد للاسم الجديد SupplierWallet
from apps.models.wallet_db import SupplierWallet 
from apps.models.supplier_db import Supplier
from sqlalchemy import or_, cast, String
from flask_paginate import Pagination, get_page_parameter

# تعريف الـ Blueprint
wallet_app = Blueprint('wallet_app', __name__, template_folder='templates')

@wallet_app.route('/', methods=['GET'])
def dashboard():
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if not request.referrer or "mahjoub.online" not in request.referrer:
            abort(403)

    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 15
    search = request.args.get('search', '')
    
    # استخدام الكلاس الجديد SupplierWallet
    query = SupplierWallet.query.join(Supplier)
    
    if search:
        query = query.filter(or_(
            Supplier.username.contains(search), # تأكد من اسم الحقل هنا (سابقاً search_name)
            Supplier.search_phone.contains(search),
            cast(SupplierWallet.id, String).contains(search)
        ))
    
    total = query.count()
    wallets = query.offset((page - 1) * per_page).limit(per_page).all()
    
    # إحصائيات المحفظة
    all_filtered = query.all()
    stats = {
        'count': total,
        'available': sum(float(w.balance_available) for w in all_filtered),
        'pending': sum(float(w.balance_pending) for w in all_filtered),
        'withdrawn': sum(float(w.total_withdrawn) for w in all_filtered)
    }
    
    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap5')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('admin/partials/wallet_table_body.html', 
                               wallets=wallets, pagination=pagination, stats=stats)
    
    return render_template('admin/wallet_app.html', 
                           wallets=wallets, pagination=pagination, stats=stats)

@wallet_app.route('/search_suppliers', methods=['GET'])
def search_suppliers():
    term = request.args.get('term', '')
    suppliers = Supplier.query.filter(
        or_(Supplier.username.contains(term), Supplier.search_phone.contains(term))
    ).limit(10).all()
    # تأكد من مطابقة الحقول هنا لما هو موجود في كلاس Supplier
    results = [{'id': s.id, 'text': f"{s.username} - {s.phone}"} for s in suppliers]
    return jsonify({'results': results})

@wallet_app.route('/manage/<int:supplier_id>', methods=['GET'])
def manage_wallet(supplier_id):
    # استخدام الكلاس الجديد SupplierWallet
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier_id).first_or_404()
    
    return render_template('admin/view_wallet.html', wallet=wallet)
