# coding: utf-8
# 📂 apps/admin_suppliers_list/routes.py

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from apps.extensions import db
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import SupplierWallet
from sqlalchemy import func

# تعريف الـ Blueprint مع تحديد مجلد القوالب
suppliers_bp = Blueprint(
    'suppliers_bp', 
    __name__, 
    template_folder='templates'
)

@suppliers_bp.route('/list')
@login_required
def list_suppliers():
    """
    عرض قائمة الموردين مع بياناتهم المالية الحقيقية.
    هذه الواجهة هي عين الإدارة على 'خزينة الموردين'.
    """
    try:
        # جلب الموردين مع دمج بيانات المحفظة (Left Join لضمان ظهور الجميع حتى لو لم يفعلوا المحفظة)
        suppliers_data = db.session.query(
            Supplier,
            SupplierWallet.balance_usd,
            SupplierWallet.balance_yer,
            SupplierWallet.balance_sar
        ).outerjoin(SupplierWallet, Supplier.id == SupplierWallet.supplier_id).all()
        
        return render_template(
            'admin_suppliers_list/admin_suppliers_list.html', 
            suppliers_data=suppliers_data
        )
    except Exception as e:
        flash("تعذر جلب بيانات الخزينة الموردين.", "error")
        return redirect(url_for('admin_bp.dashboard'))

@suppliers_bp.route('/settle/<int:supplier_id>/<string:currency>')
@login_required
def settle_supplier_funds(supplier_id, currency):
    """
    إجراء سيادي: تسوية الحسابات (إغلاق ذمة المورد من الخزينة).
    ملاحظة: هذا المسار يجب أن يُحمي بـ Admin Privilege فقط.
    """
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier_id).first()
    if not wallet:
        flash("خطأ: لا يوجد محفظة لهذا المورد.", "error")
        return redirect(url_for('suppliers_bp.list_suppliers'))

    # تنفيذ عملية التصفير (Settlement)
    if currency == 'USD': wallet.balance_usd = 0
    elif currency == 'YER': wallet.balance_yer = 0
    elif currency == 'SAR': wallet.balance_sar = 0
    
    db.session.commit()
    flash(f"✅ تم تصفية أرصدة المورد بنجاح بالعملة: {currency}", "success")
    return redirect(url_for('suppliers_bp.list_suppliers'))
