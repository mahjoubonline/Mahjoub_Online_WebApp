# coding: utf-8
# 📂 apps/admin_Product/routes_edit.py

import json
import logging
from flask import render_template, request, jsonify, flash
from flask_login import login_required
from .registry import admin_product_bp
from apps.services.graphql_client import QomrahGraphQLClient

logger = logging.getLogger(__name__)

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
            sku
            weight
            supplier_id
            pricing { 
                price 
                originalPrice 
                compareAtPrice 
                costPrice
            }
            images { 
                _id 
                fileUrl 
            }
            collections { 
                qid 
                title 
            }
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
    findAllSuppliers(input: { limit: 200 }) {
        data {
            id
            trade_name
            code
            supplier_code
        }
    }
}
"""

@admin_product_bp.route('/edit/<path:qid>', methods=['GET'])
@login_required
def edit_product(qid):
    """عرض صفحة تعديل منتج موجود بالاعتماد على معرفه (qid) مع جلب الموردين والتصنيفات."""
    product = {
        "title": "",
        "slug": "",
        "description": "",
        "status": "ACTIVE",
        "quantity": 0,
        "sku": "",
        "weight": 0,
        "supplier_id": "",
        "pricing": {"price": 0, "originalPrice": 0, "compareAtPrice": 0, "costPrice": 0},
        "images": [],
        "collection_ids": []
    }
    all_collections = []
    suppliers = []

    try:
        prod_response = QomrahGraphQLClient.execute_query(GET_PRODUCT_DETAIL_QUERY, {"qid": qid})
        col_response = QomrahGraphQLClient.execute_query(GET_ALL_COLLECTIONS_QUERY)
        sup_response = QomrahGraphQLClient.execute_query(GET_ALL_SUPPLIERS_QUERY)

        if prod_response and 'data' in prod_response:
            find_res = prod_response['data'].get('findProductByQid')
            if find_res and find_res.get('data'):
                product = find_res.get('data')

        if product:
            raw_images = product.get('images', [])
            product['images'] = [img for img in raw_images if isinstance(img, dict) and img.get('fileUrl')]
            product['collection_ids'] = [c['qid'] for c in product.get('collections', []) if c and c.get('qid')]
            
            if not product.get('pricing'):
                product['pricing'] = {"price": 0, "originalPrice": 0, "compareAtPrice": 0, "costPrice": 0}

        if col_response and 'data' in col_response:
            all_collections = col_response['data'].get('findAllCollections', {}).get('data', [])

        if sup_response and 'data' in sup_response:
            suppliers = sup_response['data'].get('findAllSuppliers', {}).get('data', [])

    except Exception as e:
        logger.error(f"❌ خطأ أثناء جلب تفاصيل المنتج للتعديل {qid}: {str(e)}")
        flash("تعذر تحميل بيانات المنتج أو القوائم المرتبطة.", "danger")

    return render_template(
        'admin/admin_edit_product.html',
        product=product,
        suppliers=suppliers,
        all_collections=all_collections
    )
