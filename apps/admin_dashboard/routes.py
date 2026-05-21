# coding: utf-8
# ⚙️ محرك تعميد الموردين - منصة محجوب أونلاين 2026

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from apps import db
from apps.models.supplier_db import Supplier

# تعريف الـ Blueprint الخاص بالموردين
# تأكد أن الاسم هنا 'add_supplier' يطابق ما تم تسجيله في __init__.py
admin_suppliers_bp = Blueprint('add_supplier', __name__)

@admin_suppliers_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_supplier_submit():
    """
    دالة معالجة تعميد (إضافة) مورد جديد
    """
    if request.method == 'POST':
        # استلام البيانات من النموذج
        try:
            name = request.form.get('name')
            wallet_code = request.form.get('wallet_code')
            
            # التحقق من وجود البيانات
            if not name or not wallet_code:
                flash('يرجى تعبئة كافة الحقول السيادية.', 'warning')
                return render_template('suppliers/add_supplier.html')

            # إنشاء المورد الجديد
            new_supplier = Supplier(name=name, wallet_code=wallet_code)
            db.session.add(new_supplier)
            db.session.commit()
            
            flash('تم تعميد شريك النجاح بنجاح.', 'success')
            return redirect(url_for('admin_dashboard.list_suppliers'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ في النظام أثناء التعميد: {str(e)}', 'danger')

    return render_template('suppliers/add_supplier.html')
