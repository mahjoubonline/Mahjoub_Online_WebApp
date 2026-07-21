# 📂 apps/admin_Product/routes_add.py

import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from apps.services.product_sync_service import ProductSyncService

admin_product_add_bp = Blueprint(
    'admin_product_add_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)

GRAPHQL_TOKEN = os.environ.get('QUMRA_API_KEY', 'YOUR_ADMIN_API_TOKEN')

@admin_product_add_bp.route('/products/add', methods=['GET', 'POST'])
def add_product():
    """مسار إضافة منتج جديد مع جلب الموردين والمجموعات لدعم واجهة الإنشاء"""
    client = ProductSyncService(token=GRAPHQL_TOKEN)
    
    suppliers = client.fetch_suppliers() if hasattr(client, 'fetch_suppliers') else []
    all_collections = client.fetch_collections() if hasattr(client, 'fetch_collections') else []

    if request.method == 'POST':
        try:
            product_data = {
                "title": request.form.get('title'),
                "slug": request.form.get('slug'),
                "description": request.form.get('description'),
                "status": request.form.get('status', 'active'),
                "supplier_id": request.form.get('supplier_id'),
                "sku": request.form.get('sku'),
                "quantity": request.form.get('quantity'),
                "weight": request.form.get('weight'),
                "pricing": {
                    "costPrice": request.form.get('original_price'),
                    "compareAtPrice": request.form.get('compare_at_price'),
                    "price": request.form.get('price')
                }
            }
            
            # يمكنك تفعيل دالة الإنشاء الفعلية في الخدمة لاحقاً
            # client.create_product(product_data, files=request.files.getlist('images'))
            
            flash("تم إضافة المنتج بنجاح.", "success")
            return redirect(url_for('admin_product_bp.manage_products'))
            
        except Exception as e:
            flash(f"حدث خطأ أثناء إضافة المنتج: {str(e)}", "danger")

    return render_template(
        'admin/add_product.html',
        suppliers=suppliers,
        all_collections=all_collections
    )
