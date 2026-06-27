# 📂 apps/suppliers_add/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from apps.models.supplier_db import Supplier
from apps.extensions import db

suppliers_add_bp = Blueprint('suppliers_add', __name__, template_folder='templates')

@suppliers_add_bp.route('/add', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        # استقبال البيانات
        username = request.form.get('username')
        trade_name = request.form.get('trade_name')
        phone = request.form.get('phone')
        password = request.form.get('password')

        if Supplier.query.filter_by(username=username).first():
            flash("اسم المستخدم موجود مسبقاً!", "danger")
            return redirect(url_for('suppliers_add.add_supplier'))

        new_supplier = Supplier(username=username, trade_name=trade_name, phone=phone, status='active')
        new_supplier.set_password(password)
        
        db.session.add(new_supplier)
        db.session.commit()
        
        flash(f"تم إضافة المورد {trade_name} بنجاح!", "success")
        return redirect(url_for('suppliers_add.add_supplier'))
        
    return render_template('suppliers_add/suppliers_add.html')
