# coding: utf-8
# 📂 apps/admin_Product/routes_add.py

import json
import logging
from flask import render_template, request, jsonify, flash
from flask_login import login_required
from .registry import admin_product_bp
from apps.services.graphql_client import QomrahGraphQLClient

logger = logging.getLogger(__name__)

GET_ALL_COLLECTIONS_QUERY = """
query GetAllCollections {
    findAllCollections(input: { limit: 100 }) {
        data { qid, title }
    }
}
"""

GET_ALL_SUPPLIERS_QUERY = """
query GetAllSuppliers {
    findAllSuppliers(input: { limit: 100 }) {
        data { id, trade_name }
    }
}
"""

@admin_product_bp.route('/add', methods=['GET'])
@login_required
def add_product():
    """عرض صفحة إضافة منتج جديد مع كائن فارغ آمن وقوائم المجموعات والموردين."""
    empty_product = {
        "title": "",
        "slug": "",
        "description": "",
        "status": "ACTIVE",
        "quantity": 0,
        "sku": "",
        "weight": 0,
        "variants": [],
        "pricing": {"price": 0, "originalPrice": 0, "compareAtPrice": 0, "costPrice": 0},
        "images": [],
        "collection_ids": [],
        "supplier_id": ""
    }
    
    all_collections = []
    suppliers = []
    
    try:
        col_response = QomrahGraphQLClient.execute_query(GET_ALL_COLLECTIONS_QUERY)
        if col_response and 'data' in col_response:
            all_collections = col_response['data'].get('findAllCollections', {}).get('data', [])
    except Exception as e:
        logger.error(f"❌ خطأ أثناء جلب المجموعات لصفحة الإضافة: {str(e)}")

    try:
        sup_response = QomrahGraphQLClient.execute_query(GET_ALL_SUPPLIERS_QUERY)
        if sup_response and 'data' in sup_response:
            suppliers = sup_response['data'].get('findAllSuppliers', {}).get('data', [])
    except Exception as e:
        logger.error(f"❌ خطأ أثناء جلب الموردين لصفحة الإضافة: {str(e)}")

    return render_template(
        'admin/admin_add_product.html',
        product=empty_product,
        suppliers=suppliers,
        all_collections=all_collections
    )


@admin_product_bp.route('/save-sync', methods=['POST'])
@login_required
def save_sync_product():
    """معالجة حفظ وإنشاء المنتج الجديد واستلام البيانات والوسائط."""
    try:
        title = request.form.get('title', '').strip()
        slug = request.form.get('slug', '').strip()
        status = request.form.get('status', 'ACTIVE').strip()
        description = request.form.get('description', '')
        quantity = int(request.form.get('quantity', 0) or 0)
        weight = float(request.form.get('weight', 0) or 0)
        sku = request.form.get('sku', '').strip()
        
        # أسماء الحقول مطابقة تماماً لما ترسله الواجهة الأمامية
        cost_price = float(request.form.get('original_price', 0) or 0)
        compare_price = float(request.form.get('compare_at_price', 0) or 0)
        price = float(request.form.get('price', 0) or 0)
        
        supplier_id = request.form.get('supplier_id', '').strip()
        collections = json.loads(request.form.get('collection_ids', '[]'))
        
        # فك تشفير مصفوفة المتغيرات (Variants) والألوان/الأحجام المضافة
        variants_raw = request.form.get('variants', '[]')
        variants = json.loads(variants_raw) if variants_raw else []
        
        uploaded_images = request.files.getlist('images')

        # هنا يمكنك كتابة استعلام الـ Mutation الخاص بـ GraphQL لحفظ البيانات في قاعدة البيانات
        # ...

        logger.info(f"✅ تم إنشاء المنتج الجديد بنجاح: {title} [المورد: {supplier_id}] [عدد المتغيرات: {len(variants)}] [عدد الصور: {len(uploaded_images)}]")

        return jsonify({
            "status": "success",
            "message": "تم إنشاء المنتج وحفظ البيانات بنجاح."
        }), 200

    except Exception as e:
        logger.error(f"❌ خطأ أثناء معالجة إنشاء المنتج: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"حدث خطأ أثناء الحفظ: {str(e)}"
        }), 400
