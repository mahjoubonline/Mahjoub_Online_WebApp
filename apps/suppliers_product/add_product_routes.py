# coding: utf-8
# 📂 apps/suppliers_product/add_product_routes.py

from flask import Blueprint, render_template, request, flash, redirect, url_for, session, abort
from flask_login import login_required, current_user
from apps.models.supplier_db import Supplier
from apps.extensions import db
import os
import traceback

# ✅ استيراد الـ Blueprint من registry.py
from apps.suppliers_product.registry import suppliers_product_bp

# ✅ تعريف Blueprint منفصل للإضافة
add_product_bp = Blueprint(
    'add_product_bp',
    __name__,
    template_folder='templates'
)


@add_product_bp.route('/add-product', methods=['GET'])
@login_required
def add_product():
    """صفحة إضافة منتج جديد للمورد"""
    try:
        user_type = session.get('user_type')
        if user_type not in ['supplier', 'staff']:
            abort(403)
        
        if user_type == 'staff':
            supplier_id = current_user.supplier_id
        else:
            supplier_id = current_user.id
        
        supplier = Supplier.query.get(supplier_id)
        if not supplier:
            abort(404)
        
        return render_template(
            'suppliers/add_product.html',
            supplier=supplier
        )
        
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"❌ خطأ في add_product: {error_details}")
        return f"❌ خطأ: {error_details}", 500


@add_product_bp.route('/add-product', methods=['POST'])
@login_required
def save_product():
    """حفظ منتج جديد للمورد"""
    try:
        user_type = session.get('user_type')
        if user_type not in ['supplier', 'staff']:
            abort(403)
        
        if user_type == 'staff':
            supplier_id = current_user.supplier_id
        else:
            supplier_id = current_user.id
        
        name = request.form.get('name', '').strip()
        cost_price = request.form.get('cost_price', '').strip()
        
        if not name:
            flash('⚠️ اسم المنتج مطلوب', 'danger')
            return redirect(url_for('add_product_bp.add_product'))
        
        if not cost_price or float(cost_price) <= 0:
            flash('⚠️ سعر التكلفة يجب أن يكون أكبر من 0', 'danger')
            return redirect(url_for('add_product_bp.add_product'))
        
        # ✅ هنا يتم رفع المنتج إلى Qumra
        # ... منطق المزامنة مع Qumra ...
        
        flash('✅ تم إضافة المنتج بنجاح، سيراجعه فريق الإدارة', 'success')
        return redirect(url_for('suppliers_product_bp.products'))
        
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"❌ خطأ في save_product: {error_details}")
        flash('❌ حدث خطأ أثناء إضافة المنتج', 'danger')
        return redirect(url_for('add_product_bp.add_product'))
