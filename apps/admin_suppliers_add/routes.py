# coding: utf-8
# 📂 apps/admin_suppliers_add/routes.py

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from apps.extensions import db
from apps.models.supplier_db import Supplier
from apps.models.supplier_staff_db import SupplierStaff
from apps.models.wallet_db import SupplierWallet  # تم الاستيراد
from sqlalchemy.exc import IntegrityError
import secrets

admin_suppliers_add_bp = Blueprint(
    'admin_suppliers_add_bp', 
    __name__, 
    template_folder='templates'
)

@admin_suppliers_add_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_supplier_or_staff():
    """نقطة دخول موحدة لإضافة مورد (مالك) أو موظف مع أتمتة المحفظة."""
    
    if request.method == 'POST':
        action_type = request.form.get('action_type') # 'owner' or 'staff'
        temp_password = secrets.token_hex(4) 
        
        try:
            if action_type == 'owner':
                # 1. إنشاء المورد (المالك)
                new_supplier = Supplier(
                    username=request.form.get('username'),
                    trade_name=request.form.get('trade_name'),
                    rank=request.form.get('rank', 'bronze'),
                    status='active'
                )
                new_supplier.phone = request.form.get('phone') 
                new_supplier.set_password(temp_password)
                
                db.session.add(new_supplier)
                db.session.commit() # حفظ المورد أولاً للحصول على ID
                
                # 2. أتمتة إنشاء المحفظة فوراً
                wallet_code = f"MAH-WEL{new_supplier.id}"
                new_wallet = SupplierWallet(
                    wallet_code=wallet_code,
                    supplier_id=new_supplier.id
                )
                db.session.add(new_wallet)
                db.session.commit()
                
                flash(f"✅ تم تسجيل المورد: {new_supplier.trade_name} | المحفظة: {wallet_code} | كلمة المرور: {temp_password}", "success")
                
            elif action_type == 'staff':
                # 3. إنشاء الموظف
                new_staff = SupplierStaff(
                    supplier_id=request.form.get('supplier_id'),
                    username=request.form.get('staff_username'),
                    phone=request.form.get('staff_phone'),
                    role='worker'
                )
                new_staff.set_password(temp_password)
                
                db.session.add(new_staff)
                db.session.commit()
                
                flash(f"✅ تم إضافة الموظف: {new_staff.username} | كلمة المرور: {temp_password}", "success")
            
            return redirect(url_for('admin_suppliers_add_bp.add_supplier_or_staff'))

        except IntegrityError:
            db.session.rollback()
            flash("❌ خطأ: اسم المستخدم أو الهاتف مسجل مسبقاً في النظام.", "danger")
        except Exception as e:
            db.session.rollback()
            flash(f"⚠️ حدث خطأ تقني: {str(e)}", "danger")

    suppliers = Supplier.query.all()
    return render_template('admin_suppliers_add/admin_suppliers_add.html', suppliers=suppliers)
