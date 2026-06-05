# 📂 apps/wallet/routes.py - المحرك المالي الاحترافي
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from sqlalchemy import func
from apps.extensions import db
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import SupplierWallet, WalletTransaction

# تعريف المحرك (Blueprint)
wallet_app = Blueprint('wallet_app', __name__)

@wallet_app.route('/view/<int:supplier_id>')
@login_required
def view_wallet(supplier_id):
    """
    عرض تفاصيل المحفظة الخاصة بمورد معين مع نظام ترقيم للعمليات
    """
    # 1. جلب بيانات المورد والمحفظة
    supplier = Supplier.query.get_or_404(supplier_id)
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier.id).first()
    
    # التحقق من وجود محفظة للمورد
    if not wallet:
        return "هذا المورد لا يمتلك محفظة حالياً.", 404

    # 2. الترقيم (Pagination): عرض 15 عملية لكل صفحة
    page = request.args.get('page', 1, type=int)
    
    # جلب العمليات مع الترقيم مرتبة من الأحدث إلى الأقدم
    pagination = WalletTransaction.query.filter_by(wallet_id=wallet.id)\
        .order_by(WalletTransaction.created_at.desc())\
        .paginate(page=page, per_page=15, error_out=False)
    
    transactions = pagination.items
    
    # 3. إرسال البيانات إلى القالب
    return render_template('admin/wallet_app_detail.html', 
                           supplier=supplier, 
                           wallet=wallet, 
                           transactions=transactions,
                           pagination=pagination)

@wallet_app.route('/stats')
@login_required
def get_stats():
    """
    إرجاع إحصائيات النظام المالية العامة بصيغة JSON
    تستخدم هذه الدالة لتحديث لوحات التحكم (Dashboards) لحظياً
    """
    # حساب إجمالي أرصدة النظام بجميع العملات
    totals = db.session.query(
        func.sum(SupplierWallet.balance_sar),
        func.sum(SupplierWallet.balance_yer),
        func.sum(SupplierWallet.balance_usd)
    ).first()
    
    # إرجاع النتائج مع معالجة القيم الفارغة (None) بتحويلها إلى 0
    return jsonify({
        'sar': float(totals[0] or 0),
        'yer': float(totals[1] or 0),
        'usd': float(totals[2] or 0)
    })
