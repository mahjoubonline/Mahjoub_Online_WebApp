# coding: utf-8
# 📂 apps/admin_Product/routes_edit.py

import json
import logging
from flask import render_template, request, jsonify, flash
from flask_login import login_required
from .registry import admin_product_bp
from apps.services.graphql_client import QomrahGraphQLClient

logger = logging.getLogger(__name__)

# --- الاستعلامات (Queries) ---
GET_PRODUCT_BY_QID_QUERY = """
query GetProductByQid($qid: String!) {
    findProductByQid(qid: $qid) {
        qid
        title
        slug
        description
        status
        quantity
        sku
        weight
        supplier_id
        collection_ids
        pricing {
            price
            originalPrice
            compareAtPrice
            costPrice
        }
        images {
            fileUrl
        }
        variants {
            name
            price
            quantity
            sku
        }
    }
}
"""

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
        data { id, trade_name, supplier_code }
    }
}
"""

# --- المتحولات (Mutations) ---
UPDATE_PRODUCT_MUTATION = """
mutation UpdateProduct($input: UpdateProductInput!) {
    updateProduct(input: $input) {
        qid
    }
}
"""


@admin_product_bp.route('/edit/<qid>', methods=['GET'])
@login_required
def edit_product(qid):
    """جلب بيانات المنتج والمجموعات والموردين وعرض صفحة التعديل."""
    product = None
    all_collections = []
    suppliers = []

    # 1. جلب بيانات المنتج المطلوب تعديله
    try:
        prod_response = QomrahGraphQLClient.execute_query(GET_PRODUCT_BY_QID_QUERY, {"qid": qid})
        if prod_response and 'data' in prod_response:
            product = prod_response['data'].get('findProductByQid')
    except Exception as e:
        logger.error(f"❌ خطأ أثناء جلب بيانات المنتج {qid}: {str(e)}")

    # 2. جلب المجموعات
    try:
        col_response = QomrahGraphQLClient.execute_query(GET_ALL_COLLECTIONS_QUERY)
        if col_response and 'data' in col_response:
            all_collections = col_response['data'].get('findAllCollections', {}).get('data', [])
    except Exception as e:
        logger.error(f"❌ خطأ أثناء جلب المجموعات: {str(e)}")

    # 3. جلب الموردين
    try:
        sup_response = QomrahGraphQLClient.execute_query(GET_ALL_SUPPLIERS_QUERY)
        if sup_response and 'data' in sup_response:
            suppliers = sup_response['data'].get('findAllSuppliers', {}).get('data', [])
    except Exception as e:
        logger.error(f"❌ خطأ أثناء جلب الموردين: {str(e)}")

    return render_template(
        'admin/admin_edit_product.html',
        product=product,
        suppliers=suppliers,
        all_collections=all_collections
    )


@admin_product_bp.route('/save-sync-update', methods=['POST'])
@login_required
def save_sync_product():
    """معالجة تحديث المنتج الحالي ومزامنة التغييرات عبر GraphQL."""
    try:
        qid = request.form.get('qid', '').strip()
        title = request.form.get('title', '').strip()
        slug = request.form.get('slug', '').strip()
        status = request.form.get('status', 'ACTIVE').strip()
        description = request.form.get('description', '')
        quantity = int(request.form.get('quantity', 0) or 0)
        weight = float(request.form.get('weight', 0) or 0)
        sku = request.form.get('sku', '').strip()
        
        cost_price = float(request.form.get('original_price', 0) or 0)
        compare_price = float(request.form.get('compare_at_price', 0) or 0)
        price = float(request.form.get('price', 0) or 0)
        
        supplier_id = request.form.get('supplier_id', '').strip()
        collections = json.loads(request.form.get('collection_ids', '[]'))
        variants = json.loads(request.form.get('variants', '[]'))
        removed_images = json.loads(request.form.get('removed_images', '[]'))

        # تجهيز Payload التحديث
        product_input = {
            "qid": qid,
            "title": title,
            "slug": slug,
            "description": description,
            "status": status,
            "quantity": quantity,
            "weight": weight,
            "sku": sku,
            "supplierId": supplier_id,
            "collectionIds": collections,
            "pricing": {
                "price": price,
                "originalPrice": cost_price,
                "compareAtPrice": compare_price
            },
            "variants": variants,
            "removedImages": removed_images
        }

        # تنفيذ التحديث عبر الـ GraphQL Client
        response = QomrahGraphQLClient.execute_mutation(UPDATE_PRODUCT_MUTATION, {"input": product_input})
        
        if response and 'errors' in response:
            error_msg = response['errors'][0]['message']
            return jsonify({"status": "error", "message": f"خطأ في الـ API: {error_msg}"}), 400

        logger.info(f"✅ تم تحديث المنتج بنجاح: {title} [QID: {qid}]")

        return jsonify({
            "status": "success",
            "message": "تم تحديث بيانات المنتج ومزامنتها بنجاح."
        }), 200

    except Exception as e:
        logger.error(f"❌ خطأ أثناء معالجة تحديث المنتج: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"حدث خطأ أثناء الحفظ: {str(e)}"
        }), 400
