# coding: utf-8
# 📂 apps/suppliers_product/add_product_routes.py

from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from apps.models.supplier_db import Supplier
from apps.extensions import db

# ✅ تعريف الـ Blueprint
add_product_bp = Blueprint(
    'add_product_bp',
    __name__,
    template_folder='templates'
)


@add_product_bp.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    """صفحة إضافة منتج جديد - يرفع المورد: الاسم، الصورة، سعر التكلفة"""
    
    # التحقق من أن المستخدم مورد
    user_type = session.get('user_type')
    if user_type not in ['supplier', 'staff']:
        flash('❌ هذا القسم مخصص للموردين فقط', 'danger')
        return redirect(url_for('suppliers_dashboard.dashboard'))
    
    supplier = Supplier.query.get(current_user.id)
    if not supplier:
        flash('❌ المورد غير موجود', 'danger')
        return redirect(url_for('suppliers_dashboard.dashboard'))
    
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            cost_price = request.form.get('cost_price', '').strip()
            image = request.files.get('image')
            
            # ✅ التحقق من البيانات
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
            print(f"❌ خطأ في add_product: {e}")
            flash(f'❌ حدث خطأ: {str(e)}', 'danger')
            return redirect(url_for('add_product_bp.add_product'))
    
    return render_template('suppliers/add_product.html', supplier=supplier)
