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

@admin_product_bp.route('/edit/<path:qid>', methods=['GET'])
@login_required
def edit_product(qid):
    """عرض صفحة تعديل منتج موجود بالاعتماد على معرفه (qid)."""
    # تهيئة كائن افتراضي لمنع حدوث UndefinedError في القالب في حال فشل الجلب
    product = {
        "title": "",
        "slug": "",
        "description": "",
        "status": "ACTIVE",
        "quantity": 0,
        "sku": "",
        "weight": 0,
        "pricing": {"price": 0, "originalPrice": 0, "compareAtPrice": 0, "costPrice": 0},
        "images": [],
        "collection_ids": []
    }
    all_collections = []

    try:
        prod_response = QomrahGraphQLClient.execute_query(GET_PRODUCT_DETAIL_QUERY, {"qid": qid})
        col_response = QomrahGraphQLClient.execute_query(GET_ALL_COLLECTIONS_QUERY)

        if prod_response and 'data' in prod_response:
            find_res = prod_response['data'].get('findProductByQid')
            if find_res and find_res.get('data'):
                product = find_res.get('data')

        if product:
            # الاحتفاظ بهيكل الصورة كاملاً (بما في ذلك fileUrl) لكي يعمل الحذف والمعاينة بشكل صحيح
            raw_images = product.get('images', [])
            product['images'] = [img for img in raw_images if isinstance(img, dict) and img.get('fileUrl')]
            product['collection_ids'] = [c['qid'] for c in product.get('collections', []) if c and c.get('qid')]
            
            # التأكد من وجود كائن pricing لتجنب أي أخطاء في القالب
            if not product.get('pricing'):
                product['pricing'] = {"price": 0, "originalPrice": 0, "compareAtPrice": 0, "costPrice": 0}

        if col_response and 'data' in col_response:
            all_collections = col_response['data'].get('findAllCollections', {}).get('data', [])

    except Exception as e:
        logger.error(f"❌ خطأ أثناء جلب تفاصيل المنتج للتعديل {qid}: {str(e)}")
        flash("تعذر تحميل بيانات المنتج.", "danger")

    return render_template(
        'admin/admin_edit_product.html',
        product=product,
        suppliers=[],
        all_collections=all_collections
    )
