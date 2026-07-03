# coding: utf-8
# 📂 apps/admin_suppliers_list/routes.py

from flask import Blueprint, render_template, jsonify, abort
from apps.models.suppliers_db import Supplier
from apps.models.supplier_profile_db import SupplierProfile
from apps.extensions import db

# تعريف الـ Blueprint
suppliers_list_bp = Blueprint(
    'suppliers_list_bp', 
    __name__, 
    template_folder='templates'
)

@suppliers_list_bp.route('/', methods=['GET'])
def list_suppliers():
    """عرض قائمة الشركاء في الجدول الرئيسي."""
    # جلب كافة الموردين مع بيانات البروفايل الخاصة بهم
    suppliers = Supplier.query.join(SupplierProfile, Supplier.id == SupplierProfile.supplier_id).all()
    return render_template('admin_suppliers_list/admin_suppliers_list.html', suppliers=suppliers)

@suppliers_list_bp.route('/details/<int:supplier_id>', methods=['GET'])
def get_supplier_details(supplier_id):
    """جلب البيانات التفصيلية للمورد لعرضها في النافذة الجديدة (Modal)."""
    # جلب المورد مع بيانات البروفايل والمحفظة
    supplier = Supplier.query.get_or_404(supplier_id)
    profile = SupplierProfile.query.filter_by(supplier_id=supplier.id).first()
    
    if not profile:
        abort(404)

    # تجهيز البيانات للنافذة الجديدة
    data = {
        "trade_name": profile.trade_name,
        "phone": supplier.phone,
        "email": profile.email,
        "governorate": profile.governorate,
        "city": profile.city,
        "rank": supplier.rank,
        "status": supplier.status,
        "id_number": profile.id_number,  # مشفر
        "bank_account": profile.bank_account # مشفر
    }
    
    return jsonify(data)
