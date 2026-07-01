# coding: utf-8
# 📂 apps/supplier_wallet/routes.py

from flask import Blueprint, render_template, abort, request
from flask_login import login_required, current_user
from flask_paginate import Pagination, get_page_parameter
from apps.models.wallet_db import SupplierWallet, WalletTransaction
from apps.api.sync_engine import SyncEngine
from datetime import datetime

# تعريف البلوبرنت الخاص بمحفظة المورد
supplier_wallet_bp = Blueprint('supplier_wallet', __name__, template_folder='templates')

@supplier_wallet_bp.route('/my-wallet', methods=['GET'])
@login_required
def view_my_wallet():
    """عرض كشف حساب المورد مع الفلترة والترقيم ودعم الـ AJAX."""
    
    # 1. جلب محفظة المورد (ضمان حماية المسار: المورد لا يرى إلا محفظته)
    wallet = SupplierWallet.query.filter_by(supplier_id=current_user.id).first()
    if not wallet:
        abort(404, description="لم يتم العثور على محفظة مرتبطة بحسابك.")

    # 2. فلتر العملة (افتراضياً SAR)
    currency = request.args.get('currency', 'SAR')
    query = WalletTransaction.query.filter_by(wallet_id=wallet.id, currency=currency)

    # 3. البحث المرن (عن سند أو وصف)
    search = request.args.get('search', '').strip()
    if search:
        query = query.filter(
            (WalletTransaction.voucher_number.ilike(f'%{search}%')) | 
            (WalletTransaction.description.ilike(f'%{search}%'))
        )

    # 4. الترتيب الزمني للأحدث
    all_transactions = query.order_by(WalletTransaction.created_at.desc()).all()
    
    # 5. حساب الإجماليات (دائن/مدين) بناءً على العملة المختارة
    # ملاحظة: نستخدم منطق تصنيف العمليات لضمان دقة الحساب
    total_credit = sum(t.amount for t in all_transactions if t.trans_type in ['sale_revenue', 'adjustment_credit'])
    total_debit = sum(t.amount for t in all_transactions if t.trans_type in ['withdrawal', 'adjustment_debit'])
    
    # 6. الترقيم (Pagination)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 20
    offset = (page - 1) * per_page
    transactions_paginated = all_transactions[offset : offset + per_page]
    
    pagination = Pagination(
        page=page, 
        total=len(all_transactions), 
        per_page=per_page, 
        css_framework='bootstrap5',
        record_name='عملية'
    )

    # 7. استجابة الـ AJAX (لتحديث الجدول فقط عند تغيير الفلتر أو الصفحة)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template(
            'supplier_wallet/_table_partial.html', 
            transactions=transactions_paginated,
            total_debit=total_debit,
            total_credit=total_credit
        )

    # 8. الاستجابة العادية (تحميل الصفحة كاملة)
    return render_template(
        'supplier_wallet/supplier_wallet.html', 
        wallet=wallet,
        transactions=transactions_paginated, 
        pagination=pagination,
        total_debit=total_debit,
        total_credit=total_credit,
        now=datetime.utcnow()
    )

@supplier_wallet_bp.route('/test-sync', methods=['GET'])
@login_required
def test_sync():
    """مسار إداري لاختبار المزامنة اليدوية."""
    if not current_user.is_admin: # فرضاً أن هناك خاصية للتحقق من الأدمن
        abort(403)
        
    success = SyncEngine.fetch_and_sync_order()
    if success:
        return "✅ تم تنفيذ عملية المزامنة بنجاح، تحقق من المحفظة."
    return "❌ فشلت عملية المزامنة، تحقق من سجلات النظام (Logs)."
