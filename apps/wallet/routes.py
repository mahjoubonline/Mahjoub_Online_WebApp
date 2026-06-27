# coding: utf-8
# 📂 apps/wallet/routes.py

from flask import Blueprint, render_template, request, abort, flash
from flask_login import login_required
from apps.models.wallet_db import SupplierWallet
from apps.models.supplier_db import Supplier
from apps import db
from sqlalchemy import or_

wallet_bp = Blueprint(
    'wallet_app', 
    __name__, 
    template_folder='templates'
)

@wallet_bp.route('/admin/dashboard', methods=['GET'])
@login_required
# @admin_required  <-- تأكد من إضافة دالة التحقق من صلاحيات الأدمن هنا
def dashboard():
    """
    لوحة تحكم المحافظ للإدارة: عرض أرصدة الموردين مع البحث المباشر
    """
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)

    # بناء استعلام البحث
    query = SupplierWallet.query.join(Supplier)
    
    if search:
        query = query.filter(or_(
            Supplier.trade_name.ilike(f'%{search}%'),
            SupplierWallet.wallet_code.ilike(f'%{search}%'),
            Supplier.search_phone.ilike(f'%{search}%')
        ))

    # التصفح (Pagination)
    wallets = query.paginate(page=page, per_page=20)
    
    # حساب الإحصائيات (يمكن تحسين هذا بجدول إحصائيات منفصل لاحقاً)
    stats = {
        'count': SupplierWallet.query.count(),
        'sar': db.session.query(db.func.sum(SupplierWallet.balance_sar)).scalar() or 0,
        'yer': db.session.query(db.func.sum(SupplierWallet.balance_yer)).scalar() or 0,
        'usd': db.session.query(db.func.sum(SupplierWallet.balance_usd)).scalar() or 0
    }

    # إذا كان الطلب Ajax (للبحث المباشر) نعيد الجزء الخاص بالجدول فقط
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('admin/wallet_table_partial.html', wallets=wallets.items, stats=stats)

    return render_template('admin/wallet_app.html', wallets=wallets.items, stats=stats, pagination=wallets)

@wallet_bp.route('/admin/manage/<int:supplier_id>', methods=['GET'])
@login_required
def manage_wallet(supplier_id):
    """
    عرض كشف حركة محفظة مورد محدد
    """
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier_id).first_or_404()
    # هنا سنعرض سجل العمليات (Transactions) لاحقاً
    return render_template('admin/wallet_details.html', wallet=wallet)
