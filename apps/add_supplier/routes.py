# coding: utf-8
# ⚙️ محرك تعميد وإدارة الموردين - منصة محجوب أونلاين 2026

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from . import admin_suppliers_bp
from apps.models.supplier_db import Supplier
from apps import db

@admin_suppliers_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_supplier_submit():
    """
    مسار تعميد مورد جديد - متطابق مع استدعاء: url_for('add_supplier.add_supplier_submit')
    """
    if request.method == 'POST':
        # منطق معالجة البيانات (تأكد من مطابقة أسماء الحقول في الفورم)
        try:
            name = request.form.get('name')
            wallet_code = request.form.get('wallet_code')
            
            # مثال لإنشاء المورد (تأكد من أن الموديل يحتوي على هذه الحقول)
            new_supplier = Supplier(name=name, wallet_code=wallet_code)
            db.session.add(new_supplier)
            db.session.commit()
            
            flash("تم تعميد المورد بنظام السيادة بنجاح", "success")
            return redirect(url_for('admin_dashboard.list_suppliers'))
        except Exception as e:
            db.session.rollback()
            flash(f"حدث خطأ سيادي: {str(e)}", "danger")
        
    return render_template('add_supplier/add_supplier.html')

# تعيين الاسم القديم كـ Alias لتجنب أي أخطاء في الروابط القديمة
add_supplier_route = add_supplier_submit

@admin_suppliers_bp.route('/list', methods=['GET'])
@login_required
def list_suppliers_data():
    """
    مسار جلب قائمة الموردين
    """
    suppliers = Supplier.query.all()
    return render_template('add_supplier/list.html', suppliers=suppliers)
