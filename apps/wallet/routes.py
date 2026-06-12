# coding: utf-8
from flask import Blueprint, render_template, request, jsonify, abort
from apps.models.wallet_db import SupplierWallet, WalletTransaction
from apps.models.supplier_db import Supplier
from sqlalchemy import or_, cast, String
from flask_paginate import Pagination, get_page_parameter

# تعريف الـ Blueprint
# المسارات هنا تبدأ من بعد الـ url_prefix المعرف في __init__.py وهو /wallet
wallet_app = Blueprint('wallet_app', __name__, template_folder='templates')

@wallet_app.route('/', methods=['GET'])
def dashboard():
    # حماية: التأكد أن الطلبات القادمة عبر AJAX هي من موقعك فقط
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if not request.referrer or "mahjoub.online" not in request.referrer:
            abort(403)

    # 1. إعداد متغيرات الترقيم
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 15
    search = request.args.get('search', '')
    
    # 2. بناء الاستعلام مع ربط جدول الموردين
    query = SupplierWallet.query.join(Supplier)
    
    if search:
        query = query.filter(or_(
            Supplier.search_name.contains(search),
            Supplier.search_phone.contains(search),
            cast(SupplierWallet.id, String).contains(search)
        ))
    
    # 3. حساب الإجمالي للترقيم
    total = query.count()
    
    # جلب البيانات الخاصة بالصفحة الحالية فقط
    wallets = query.offset((page - 1) * per_page).limit(per_page).all()
    
    # 4. حساب الإحصائيات (Stats) برمجياً - تجنب func.sum بسبب التشفير
    all_filtered = query.all()
    stats = {
        'count': total,
        'sar': sum(float(w.balance_sar) for w in all_filtered),
        'yer': sum(float(w.balance_yer) for w in all_filtered),
        'usd': sum(float(w.balance_usd) for w in all_filtered)
    }
    
    # 5. تهيئة الترقيم
    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap5')
    
    # 6. إذا كان الطلب AJAX نعيد فقط الـ Partial
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('admin/partials/wallet_table_body.html', 
                               wallets=wallets, 
                               pagination=pagination,
                               stats=stats)
    
    # إذا كان الطلب عادياً، نعيد الصفحة كاملة
    return render_template('admin/wallet_app.html', 
                           wallets=wallets, 
                           pagination=pagination,
                           stats=stats)

@wallet_app.route('/search_suppliers', methods=['GET'])
def search_suppliers():
    term = request.args.get('term', '')
    suppliers = Supplier.query.filter(
        or_(Supplier.search_name.contains(term), Supplier.search_phone.contains(term))
    ).limit(10).all()
    results = [{'id': s.id, 'text': f"{s.trade_name} - {s.owner_phone}"} for s in suppliers]
    return jsonify({'results': results})

@wallet_app.route('/manage/<int:supplier_id>', methods=['GET'])
def manage_wallet(supplier_id):
    # جلب المحفظة
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier_id).first_or_404()
    
    # التقاط فلاتر التواريخ
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # جلب الحركات الخاصة بهذه المحفظة
    query = WalletTransaction.query.filter_by(wallet_id=wallet.id)
    
    if start_date:
        query = query.filter(WalletTransaction.created_at >= start_date)
    if end_date:
        query = query.filter(WalletTransaction.created_at <= end_date)
    
    transactions = query.order_by(WalletTransaction.created_at.desc()).all()
    
    return render_template('admin/view_wallet.html', 
                           wallet=wallet, 
                           transactions=transactions)
