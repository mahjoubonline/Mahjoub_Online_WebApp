# 📂 apps/admin_suppliers_add/routes.py
import secrets
import logging
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required
from apps.extensions import db
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import SupplierWallet

# إعداد الـ Blueprint
admin_suppliers_add_bp = Blueprint('admin_suppliers_add_bp', __name__, template_folder='templates')

@admin_suppliers_add_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_supplier_or_staff():
    if request.method == 'POST':
        try:
            # استقبال البيانات
            owner_name = request.form.get('owner_name', '').strip()
            username = request.form.get('username', '').strip()
            trade_name = request.form.get('trade_name', '').strip()
            phone = request.form.get('phone', '').strip()
            
            # توليد كلمة مرور عشوائية قوية
            temp_password = secrets.token_hex(4)

            # التحقق من وجود المستخدم مسبقاً
            if Supplier.query.filter((Supplier.username == username) | (Supplier.phone == phone)).first():
                flash("اسم المستخدم أو رقم الهاتف مستخدم مسبقاً", "danger")
                return redirect(url_for('admin_suppliers_add_bp.add_supplier_or_staff'))

            # إنشاء المورد
            new_supplier = Supplier(
                owner_name=owner_name,
                username=username,
                trade_name=trade_name,
                phone=phone,
                status='active',
                created_at=datetime.utcnow()
            )
            new_supplier.set_password(temp_password)
            
            db.session.add(new_supplier)
            db.session.flush() # هام: للحصول على الـ ID قبل الـ Commit

            # إنشاء المحفظة
            wallet_code = f"MAH-{new_supplier.id}-WEL"
            new_wallet = SupplierWallet(supplier_id=new_supplier.id, wallet_code=wallet_code)
            db.session.add(new_wallet)
            
            db.session.commit()
            
            # تخزين البيانات في الجلسة لعرضها في النافذة المنبثقة
            session['new_user_data'] = {
                'trade_name': trade_name,
                'username': username,
                'password': temp_password,
                'wallet_code': wallet_code
            }
            
            return redirect(url_for('admin_suppliers_add_bp.add_supplier_or_staff'))

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error saving supplier: {str(e)}")
            flash("حدث خطأ تقني، يرجى المحاولة لاحقاً", "danger")
            return redirect(url_for('admin_suppliers_add_bp.add_supplier_or_staff'))

    # معالجة عرض الصفحة
    new_user = session.pop('new_user_data', None)
    return render_template('admin_suppliers_add/admin_suppliers_add.html', new_user=new_user)
