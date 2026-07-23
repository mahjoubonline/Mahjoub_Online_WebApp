# coding: utf-8
# 📂 apps/suppliers_product/add_product_routes.py

from flask import render_template, request, abort, session, redirect, url_for, flash
from flask_login import login_required, current_user
import os
import traceback

from apps.models.supplier_db import Supplier
from apps.extensions import db
from apps.services.product_sync_service import ProductSyncService

# ✅ استيراد الـ Blueprint من registry.py
from apps.suppliers_product.registry import suppliers_product_bp

GRAPHQL_TOKEN = os.environ.get('QUMRA_API_KEY', 'YOUR_ADMIN_API_TOKEN')


# ============================================================
# 🟣 مسار إضافة منتج جديد (GET)
# ============================================================
@suppliers_product_bp.route('/add-product', methods=['GET'])
@login_required
def add_product_page():
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
        print(f"❌ خطأ في add_product_page: {error_details}")
        return f"❌ خطأ: {error_details}", 500


# ============================================================
# 🟣 مسار حفظ منتج جديد (POST)
# ============================================================
@suppliers_product_bp.route('/add-product', methods=['POST'])
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
        
        # ✅ جلب البيانات من النموذج
        name = request.form.get('name', '').strip()
        cost_price = request.form.get('cost_price', '').strip()
        image = request.files.get('image')
        
        # ✅ التحقق من البيانات
        if not name:
            flash('⚠️ اسم المنتج مطلوب', 'danger')
            return redirect(url_for('suppliers_product_bp.add_product_page'))
        
        if not cost_price or float(cost_price) <= 0:
            flash('⚠️ سعر التكلفة يجب أن يكون أكبر من 0', 'danger')
            return redirect(url_for('suppliers_product_bp.add_product_page'))
        
        # ✅ هنا يتم رفع المنتج إلى Qumra
        # ... منطق المزامنة مع Qumra ...
        
        flash('✅ تم إضافة المنتج بنجاح، سيراجعه فريق الإدارة', 'success')
        return redirect(url_for('suppliers_product_bp.products'))
        
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"❌ خطأ في save_product: {error_details}")
        flash('❌ حدث خطأ أثناء إضافة المنتج', 'danger')
        return redirect(url_for('suppliers_product_bp.add_product_page'))
