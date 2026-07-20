# coding: utf-8
# 📂 apps/admin_Product/routes.py

import json
import logging
import urllib.parse
from flask import render_template, request, jsonify, flash
from flask_login import login_required
from .registry import admin_product_bp
from apps.services.graphql_client import QomrahGraphQLClient

logger = logging.getLogger(__name__)

# --- الاستعلامات (Queries) ---
GET_ALL_PRODUCTS_QUERY = """
query Data($input: GetAllProductsInput) {
    findAllProducts(input: $input) {
        data {
            qid
            title
            pricing { price }
            quantity
            images { fileUrl }
        }
        pagination { currentPage, totalPages }
    }
}
"""

GET_PRODUCT_DETAIL_QUERY = """
query GetProductDetail($qid: String!) {  
    findProductByQid(qid: $qid) {  
        data {
            qid
            title
            slug
            description
            status
            quantity
            pricing { price, originalPrice, compareAtPrice }
            images { _id, fileUrl }
            collections { qid, title }
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

# --- المتحولات (Mutations) ---
CREATE_PRODUCT_MUTATION = """
mutation CreateProduct($input: CreateProductInput!) {
    createProduct(input: $input) { qid }
}
"""

UPDATE_PRODUCT_MUTATION = """
mutation UpdateProduct($qid: ID!, $input: UpdateProductInput!) {
    updateProduct(qid: $qid, input: $input) { qid }
}
"""

@admin_product_bp.route('/', methods=['GET'])
@login_required
def manage_products():
    """راوتر واجهة عرض المنتجات والبحث والتنقل بين الصفحات."""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('title', '').strip()
    
    products = []
    pagination = {"currentPage": page, "totalPages": 1}
    
    try:
        input_data = {"page": page, "limit": 50}
        if search:
            input_data["title"] = search
            
        response = QomrahGraphQLClient.execute_query(GET_ALL_PRODUCTS_QUERY, {"input": input_data})
        if response and 'data' in response:
            result = response['data'].get('findAllProducts', {})
            products = result.get('data') or []
            pagination = result.get('pagination') or {"currentPage": page, "totalPages": 1}
    except Exception as e:
        logger.error(f"❌ خطأ في جلب قائمة المنتجات: {str(e)}")
        flash("حدث خطأ أثناء تحميل قائمة المنتجات.")

    return render_template('admin/admin_Product.html', products=products, pagination=pagination, search=search)


@admin_product_bp.route('/add', methods=['GET'])
@login_required
def add_product():
    """عرض صفحة إضافة منتج جديد."""
    empty_product = {
        "title": "", "slug": "", "description": "", "status": "ACTIVE",
        "quantity": 0, "pricing": {"price": 0, "originalPrice": 0, "compareAtPrice": 0},
        "images": [], "collection_ids": []
    }
    
    all_collections = []
    try:
        col_response = QomrahGraphQLClient.execute_query(GET_ALL_COLLECTIONS_QUERY)
        if col_response and 'data' in col_response:
            all_collections = col_response['data'].get('findAllCollections', {}).get('data', [])
    except Exception as e:
        logger.error(f"❌ خطأ أثناء جلب المجموعات لصفحة الإضافة: {str(e)}")

    return render_template('admin/admin_add_product.html', product=empty_product, all_collections=all_collections)


@admin_product_bp.route('/edit/<path:qid>', methods=['GET'])
@login_required
def edit_product(qid):
    """عرض صفحة تعديل منتج."""
    decoded_qid = urllib.parse.unquote(qid)
    product = {"qid": decoded_qid, "title": "", "slug": "", "description": "", "status": "ACTIVE", "quantity": 0, "pricing": {"price": 0, "originalPrice": 0, "compareAtPrice": 0}, "images": [], "collection_ids": []}
    all_collections = []

    try:
        prod_response = QomrahGraphQLClient.execute_query(GET_PRODUCT_DETAIL_QUERY, {"qid": decoded_qid})
        col_response = QomrahGraphQLClient.execute_query(GET_ALL_COLLECTIONS_QUERY)

        if prod_response and 'data' in prod_response:
            find_res = prod_response['data'].get('findProductByQid')
            if find_res and find_res.get('data'):
                product = find_res.get('data')
                product['images'] = [img.get('fileUrl') for img in product.get('images', []) if isinstance(img, dict)]
                product['collection_ids'] = [c['qid'] for c in product.get('collections', []) if c and c.get('qid')]

        if col_response and 'data' in col_response:
            all_collections = col_response['data'].get('findAllCollections', {}).get('data', [])
    except Exception as e:
        logger.error(f"❌ خطأ أثناء جلب تفاصيل المنتج للتعديل {decoded_qid}: {str(e)}")
        flash("تعذر تحميل بيانات المنتج.", "danger")

    return render_template('admin/admin_add_product.html', product=product, all_collections=all_collections)


@admin_product_bp.route('/save-sync', methods=['POST'])
@login_required
def save_sync():
    """معالجة حفظ وإنشاء أو تحديث المنتج."""
    try:
        qid = request.form.get('qid', '').strip()
        input_data = {
            "title": request.form.get('title'),
            "slug": request.form.get('slug'),
            "description": request.form.get('description'),
            "status": request.form.get('status', 'ACTIVE'),
            "quantity": int(request.form.get('quantity', 0)),
            "pricing": {"price": float(request.form.get('price', 0))},
            "collectionIds": json.loads(request.form.get('collection_ids', '[]'))
        }

        if qid:
            # تنفيذ التحديث
            QomrahGraphQLClient.execute_mutation(UPDATE_PRODUCT_MUTATION, {"qid": qid, "input": input_data})
            message = "تم تحديث المنتج بنجاح."
        else:
            # تنفيذ الإنشاء
            QomrahGraphQLClient.execute_mutation(CREATE_PRODUCT_MUTATION, {"input": input_data})
            message = "تم إنشاء المنتج بنجاح."

        return jsonify({"status": "success", "message": message}), 200

    except Exception as e:
        logger.error(f"❌ خطأ أثناء حفظ المنتج: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 400
