# coding: utf-8
# 📂 apps/admin_suppliers_list/routes.py

from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
from apps.extensions import db
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import SupplierWallet

# 1. إنشاء الـ Blueprint بالاسم الذي يتطابق مع الـ registry.py
suppliers_bp = Blueprint(
    'suppliers_bp', 
    __name__, 
    template_folder='templates'
)

# 2. مسار قائمة الموردين
@suppliers_bp.route('/list', methods=['GET'])
@login_required
def list_suppliers():
    """عرض قائمة الشركاء المعتمدين."""
    try:
        # جلب الموردين من قاعدة البيانات
        suppliers = Supplier.query.all()
        return render_template(
            'admin_suppliers_list/admin_suppliers_list.html', 
            suppliers=suppliers
        )
    except Exception as e:
        flash(f"خطأ في تحميل البيانات: {str(e)}", "danger")
        return redirect(url_for('admin_dashboard_bp.dashboard'))

# 3. مسار إضافة شريك جديد (يتم استدعاؤه عبر url_for('suppliers_bp.add_supplier'))
@suppliers_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_supplier():
    # هنا ستضع منطق صفحة الإضافة الخاصة بك
    return "صفحة إضافة شريك جديد - قيد الإنشاء"

# 4. مسار تفاصيل الشريك (يتم استدعاؤه عبر url_for('suppliers_bp.supplier_details', ...))
@suppliers_bp.route('/details/<int:supplier_id>', methods=['GET'])
@login_required
def supplier_details(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    return f"تفاصيل الشريك: {supplier.name}"

# 5. مسار التصفية المالية
@suppliers_bp.route('/settle/<int:supplier_id>/<string:currency>', methods=['POST', 'GET'])
@login_required
def settle_supplier_funds(supplier_id, currency):
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier_id).first()
    if not wallet:
        flash("خطأ: المحفظة غير موجودة.", "danger")
        return redirect(url_for('suppliers_bp.list_suppliers'))

    # التصفية السيادية
    if currency == 'USD': wallet.balance_usd = 0
    elif currency == 'YER': wallet.balance_yer = 0
    elif currency == 'SAR': wallet.balance_sar = 0
    
    db.session.commit()
    flash(f"✅ تمت التصفية لعملة {currency}", "success")
    return redirect(url_for('suppliers_bp.list_suppliers'))
