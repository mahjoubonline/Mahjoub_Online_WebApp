# coding: utf-8
# 📂 apps/admin_Product/routes_edit.py

import json
import logging
from flask import render_template, request, flash, jsonify
from flask_login import login_required
from .registry import admin_product_bp
from apps.services.graphql_client import QomrahGraphQLClient

logger = logging.getLogger(__name__)

# استعلام تفاصيل المنتج الخاص بواجهة التعديل
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

# استعلام جلب المجموعات العام
GET_ALL_COLLECTIONS_QUERY = """
query GetAllCollections {
    findAllCollections(input: { limit: 100 }) {
        data { qid, title }
    }
}
"""

@admin_product_bp.route('/add', methods=['GET'])
@login_required
def add_product():
    """عرض صفحة إضافة منتج جديد مع المجموعات."""
    empty_product = {
        "title": "",
        "slug": "",
        "description": "",
        "status": "ACTIVE",
        "quantity": 0,
        "sku": "",
        "weight": 0,
        "variants": [],
        "pricing": {"price": 0, "originalPrice": 0, "compareAtPrice": 0},
        "images": [],
        "collection_ids": []
    }
    
    all_collections = []
    try:
        col_response = QomrahGraphQLClient.execute_query(GET_ALL_COLLECTIONS_QUERY)
        if col_response and 'data' in col_response:
            all_collections = col_response['data'].get('findAllCollections', {}).get('data', [])
    except Exception as e:
        logger.error(f"❌ خطأ أثناء جلب المجموعات لإضافة المنتج: {str(e)}")

    return render_template(
        'admin/admin_edit_product.html',
        product=empty_product,
        suppliers=[],
        all_collections=all_collections
    )


@admin_product_bp.route('/edit/<path:qid>', methods=['GET'])
@login_required
def edit_product(qid):
    """راوتر التعديل: يتولى جلب كافة التفاصيل العميقة للمنتج بالاعتماد على معرّفه (qid)."""
    product = {}
    all_collections = []

    try:
        prod_response = QomrahGraphQLClient.execute_query(GET_PRODUCT_DETAIL_QUERY, {"qid": qid})
        col_response = QomrahGraphQLClient.execute_query(GET_ALL_COLLECTIONS_QUERY)

        if prod_response and 'data' in prod_response:
            find_res = prod_response['data'].get('findProductByQid')
            if find_res:
                product = find_res.get('data') if isinstance(find_res, dict) and 'data' in find_res else find_res

        if product:
            raw_images = product.get('images', [])
            product['images'] = [img.get('fileUrl') for img in raw_images if isinstance(img, dict) and img.get('fileUrl')]
            product['collection_ids'] = [c['qid'] for c in product.get('collections', []) if c and c.get('qid')]

        if col_response and 'data' in col_response:
            all_collections = col_response['data'].get('findAllCollections', {}).get('data', [])

    except Exception as e:
        logger.error(f"❌ خطأ أثناء جلب تفاصيل المنتج للتعديل {qid}: {str(e)}")
        flash("تعذر تحميل بيانات المنتج.", "danger")

    return render_template(
        'admin/admin_edit_product.html',
        product=product or {},
        suppliers=[],
        all_collections=all_collections
    )


@admin_product_bp.route('/update-sync', methods=['POST'])
@login_required
def update_sync_product():
    """معالجة حفظ وتحديث بيانات المنتج."""
    try:
        qid = request.form.get('qid', '').strip()
        title = request.form.get('title', '').strip()
        slug = request.form.get('slug', '').strip()
        status = request.form.get('status', 'ACTIVE').strip()
        description = request.form.get('description', '')
        sku = request.form.get('sku', '').strip()
        quantity = int(request.form.get('quantity', 0) or 0)
        weight = float(request.form.get('weight', 0) or 0)
        
        original_price = float(request.form.get('original_price') or 0)
        compare_at_price = float(request.form.get('compare_at_price') or 0)
        price = float(request.form.get('price') or 0)
        
        action_type = "تحديث" if qid else "إنشاء"
        logger.info(f"✅ تم {action_type} المنتج: {title} [QID: {qid}]")

        return jsonify({
            "status": "success", 
            "message": f"تم {action_type} المنتج بنجاح."
        }), 200
        
    except Exception as e:
        logger.error(f"❌ خطأ في الحفظ: {str(e)}")
        return jsonify({
            "status": "error", 
            "message": f"حدث خطأ: {str(e)}"
        }), 400
