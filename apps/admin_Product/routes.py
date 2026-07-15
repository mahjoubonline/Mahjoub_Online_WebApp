# 📂 apps/admin_Product/routes.py

from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required
from apps.models.product_db import Product

# تعريف البلوبرينت
admin_product_bp = Blueprint(
    'admin_product', 
    __name__, 
    template_folder='templates'
)

@admin_product_bp.route('/', methods=['GET'])
@login_required
def manage_products():
    """عرض قائمة المنتجات بنظام الصفحات (Pagination)"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    pagination = Product.query.order_by(Product.created_at.desc()).paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return render_template(
        'admin/admin_Product.html', 
        products=pagination.items,
        pagination=pagination
    )

@admin_product_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    """
    تم التعديل: هذا المسار الآن يفتح صفحة قائمة المنتجات (admin_Product.html)
    مباشرة بدلاً من البحث عن صفحة الإضافة.
    """
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    pagination = Product.query.order_by(Product.created_at.desc()).paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    # نقوم باستدعاء صفحة admin_Product.html مباشرة
    return render_template(
        'admin/admin_Product.html', 
        products=pagination.items,
        pagination=pagination
    )

@admin_product_bp.route('/sync', methods=['POST'])
@login_required
def sync_products():
    """مسار خاص ببدء المزامنة"""
    return jsonify({"status": "success", "message": "بدء عملية المزامنة..."})
