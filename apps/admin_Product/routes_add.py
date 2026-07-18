# apps/admin_Product/routes_add.py

# coding: utf-8
from flask import render_template
from flask_login import login_required
from .routes import admin_product_bp

@admin_product_bp.route('/add', methods=['GET'])
@login_required
def add_product():
    """
    راوتر لعرض صفحة إضافة منتج.
    يستخدم الـ Blueprint المعرف في routes.py لمنع التعارضات.
    """
    return render_template('admin/admin_add_product.html', product=None)
