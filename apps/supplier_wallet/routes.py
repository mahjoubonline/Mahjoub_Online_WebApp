# coding: utf-8
# 📂 apps/supplier_wallet/routes.py

from flask import Blueprint, render_template, abort, request
from flask_login import login_required, current_user
from flask_paginate import Pagination, get_page_parameter
from apps.supplier_wallet.services import WalletService

supplier_wallet_bp = Blueprint(
    'supplier_wallet', 
    __name__, 
    template_folder='templates'
)

@supplier_wallet_bp.route('/my-wallet', methods=['GET'])
@login_required
def view_my_wallet():
    # 1. جلب المحفظة الخاصة بالمورد الحالي
    wallet = getattr(current_user, 'wallet', None)
    if not wallet:
        wallet = WalletService.get_supplier_wallet(current_user.id)
    
    if not wallet:
        abort(404, description="لم يتم العثور على محفظة مرتبطة بحسابك.")

    # 2. إعداد الترقيم (Pagination)
    # جلب كافة حركات المحفظة مرتبة حسب التاريخ (الأحدث أولاً)
    all_transactions = sorted(wallet.transactions, key=lambda x: x.created_at, reverse=True)
    
    # تحديد الصفحة الحالية وعدد العناصر في كل صفحة
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10  # عرض 10 حركات لكل صفحة
    offset = (page - 1) * per_page
    
    # استخراج الحركات الخاصة بالصفحة الحالية فقط (لضمان سرعة الأداء)
    transactions_paginated = all_transactions[offset : offset + per_page]
    
    # تهيئة كائن الترقيم
    pagination = Pagination(
        page=page, 
        total=len(all_transactions), 
        per_page=per_page, 
        css_framework='bootstrap5',
        record_name='حركات'
    )

    # 3. حساب الإجماليات (محرك المحاسبة)
    # يتم حسابها بناءً على كامل حركات المحفظة وليس فقط الحركات المعروضة في الصفحة الحالية
    total_debit = sum(t.amount for t in wallet.transactions if t.trans_type == 'debit')
    total_credit = sum(t.amount for t in wallet.transactions if t.trans_type == 'credit')

    # 4. تمرير البيانات للقالب
    return render_template(
        'supplier_wallet/supplier_wallet.html', 
        wallet=wallet,
        transactions=transactions_paginated, 
        pagination=pagination,
        total_debit=total_debit,
        total_credit=total_credit
    )
