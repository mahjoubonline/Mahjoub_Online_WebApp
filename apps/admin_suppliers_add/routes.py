# coding: utf-8
# 📂 apps/admin_suppliers_add/routes.py

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from apps.extensions import db
from apps.models.suppliers_db import Supplier
from apps.models.supplier_staff_db import SupplierStaff
from sqlalchemy.exc import IntegrityError

admin_suppliers_add_bp = Blueprint(
    'admin_suppliers_add_bp', 
    __name__, 
    template_folder='templates'
)

@admin_suppliers_add_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_supplier_or_staff():
    """نقطة دخول موحدة لإضافة مورد جديد (مالك) أو موظف تابع لمورد."""
    
    if request.method == 'POST':
        action_type = request.form.get('action_type') # 'owner' or 'staff'
        
        try:
            if action_type == 'owner':
                # منطق تسجيل المالك (المورد الأساسي)
                new_supplier = Supplier(
                    username=request.form.get('username'),
                    trade_name=request.form.get('trade_name'),
                    status='active'
                )
                new_supplier.phone = request.form.get('phone') # التشفير يتم في الـ Setter
                new_supplier.set_password(request.form.get('password'))
                
                db.session.add(new_supplier)
                db.session.commit()
                flash(f"تم تسجيل المورد {new_supplier.trade_name} بنجاح.", "success")
                
            elif action_type == 'staff':
                # منطق تسجيل موظف تابع لمورد
                supplier_id = request.form.get('supplier_id')
                new_staff = SupplierStaff(
                    supplier_id=supplier_id,
                    username=request.form.get('username'),
                    email=request.form.get('email'),
                    role=request.form.get('role', 'worker')
                )
                new_staff.set_password(request.form.get('password'))
                
                db.session.add(new_staff)
                db.session.commit()
                flash("تم إضافة الموظف بنجاح.", "success")
            
            return redirect(url_for('admin_suppliers_add_bp.add_supplier_or_staff'))

        except IntegrityError:
            db.session.rollback()
            flash("خطأ: اسم المستخدم أو البريد الإلكتروني مسجل مسبقاً.", "danger")
        except Exception as e:
            db.session.rollback()
            flash(f"حدث خطأ تقني: {str(e)}", "danger")

    # جلب قائمة الموردين لاستخدامها في حال اختيار إضافة موظف
    suppliers = Supplier.query.all()
    return render_template('admin_suppliers_add/admin_suppliers_add.html', suppliers=suppliers)
