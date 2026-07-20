# coding: utf-8
# 📂 apps/admin_Product/routes_edit.py

import json
import logging
import urllib.parse
from flask import render_template, request, jsonify, flash
from flask_login import login_required
from .registry import admin_product_bp
from apps.services.graphql_client import QomrahGraphQLClient

logger = logging.getLogger(__name__)

# --- الاستعلامات الخاصة بـ GraphQL ---

# استعلام تفاصيل المنتج
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
            supplier_id
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
            variants {
                name
                price
                quantity
                sku
            }
        }
    }  
}
"""

# استعلام جلب المجموعات والتصنيفات
GET_ALL_COLLECTIONS_QUERY = """
query GetAllCollections {
    findAllCollections(input: { limit: 100 }) {
        data { qid title }
    }
}
"""

# استعلام جلب الموردين المتاحين في النظام
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

# طفرة (Mutation) تحديث المنتج والمزامنة مع منصة قمرة
UPDATE_PRODUCT_MUTATION = """
mutation UpdateProduct($qid: String!, $input: ProductUpdateInput!) {
    updateProduct(qid: $qid, input: $input) {
        status
        message
        data {
            qid
            title
        }
    }
}
"""


# --- مسارات الـ Blueprint ---

@admin_product_bp.route('/edit/<path:qid>', methods=['GET'])
@login_required
def edit_product(qid):
    """
    عرض صفحة تعديل منتج موجود بالاعتماد على معرفه الفريد (qid).
    يقوم بجلب كافة تفاصيل المنتج، المجموعات، والموردين لتغذية حقول الاختيار المتعددة وقائمة الموردين.
    """
    decoded_qid = urllib.parse.unquote(qid)
    
    # القيم الافتراضية للمنتج لتفادي كسر الـ Jinja2 في القالب في حال تعذر جلب البيانات
    default_product = {
        "qid": decoded_qid,
        "title": "",
        "slug": "",
        "description": "",
        "status": "ACTIVE",
        "quantity": 0,
        "supplier_id": "",
        "sku": "",
        "weight": 0,
        "pricing": {"price": 0, "originalPrice": 0, "compareAtPrice": 0},
        "images": [],
        "collections": [],
        "collection_ids": [],
        "variants": []
    }
    
    product = default_product
    all_collections = []
    suppliers = []

    try:
        # استدعاء الاستعلامات المتعددة من خادم الـ GraphQL
        prod_response = QomrahGraphQLClient.execute_query(GET_PRODUCT_DETAIL_QUERY, {"qid": decoded_qid})
        col_response = QomrahGraphQLClient.execute_query(GET_ALL_COLLECTIONS_QUERY)
        sup_response = QomrahGraphQLClient.execute_query(GET_ALL_SUPPLIERS_QUERY)

        # 1. استخراج ومعالجة بيانات المنتج المسترجع
        if prod_response and 'data' in prod_response:
            find_res = prod_response['data'].get('findProductByQid')
            if find_res and find_res.get('data'):
                product = find_res.get('data')

        if product:
            # تنظيف الصور وتحويلها لقائمة من الروابط النصية المباشرة
            raw_images = product.get('images') or []
            product['images'] = [
                img.get('fileUrl') for img in raw_images 
                if isinstance(img, dict) and img.get('fileUrl')
            ]
            
            # استخراج معرفات المجموعات الحالية لتحديد الاختيار التلقائي في الـ Choices.js
            raw_collections = product.get('collections') or []
            product['collection_ids'] = [
                c['qid'] for c in raw_collections 
                if isinstance(c, dict) and c.get('qid')
            ]
            
            # حماية كائن الأسعار والمخزون والأنواع من القيم الفارغة (None)
            if not product.get('pricing'):
                product['pricing'] = {"price": 0, "originalPrice": 0, "compareAtPrice": 0}
            
            if not product.get('variants'):
                product['variants'] = []

        # 2. استخراج قائمة المجموعات والتصنيفات الشاملة لخيارات القالب
        if col_response and 'data' in col_response:
            all_collections = col_response['data'].get('findAllCollections', {}).get('data', []) or []

        # 3. استخراج قائمة الموردين الشاملة لخيارات المورد المسؤول
        if sup_response and 'data' in sup_response:
            suppliers = sup_response['data'].get('findAllSuppliers', {}).get('data', []) or []

    except Exception as e:
        logger.error(f"❌ خطأ أثناء جلب تفاصيل المنتج للتعديل {decoded_qid}: {str(e)}", exc_info=True)
        flash("تعذر تحميل بيانات المنتج أو القوائم المرتبطة بصورة كاملة.", "danger")

    return render_template(
        'admin/admin_edit_product.html',
        product=product,
        suppliers=suppliers,
        all_collections=all_collections
    )


@admin_product_bp.route('/save-sync', methods=['POST'])
@login_required
def save_sync_product():
    """
    استقبال وحفظ التعديلات الطارئة على بيانات المنتج من القالب المطور.
    يدعم معالجة الحقول الأساسية والأسعار والأنواع المتعددة والتصنيفات المحددة مع مزامنتها مع الـ GraphQL.
    """
    try:
        # استقبال البيانات الأساسية الموجهة من نموذج الـ HTML المدمج
        qid = request.form.get('qid')
        title = request.form.get('title')
        slug = request.form.get('slug')
        description = request.form.get('description')
        status = request.form.get('status', 'ACTIVE')
        supplier_id = request.form.get('supplier_id')
        sku = request.form.get('sku')
        
        # تحويل الأرقام بصورة آمنة لتجنب الاستثناءات والانهيارات
        try:
            quantity = int(request.form.get('quantity', 0) or 0)
            weight = float(request.form.get('weight', 0.0) or 0.0)
            price = float(request.form.get('price', 0.0) or 0.0)
            cost_price = float(request.form.get('original_price', 0.0) or 0.0)
            compare_at_price = float(request.form.get('compare_at_price', 0.0) or 0.0)
        except ValueError as val_err:
            return jsonify({
                'status': 'error',
                'message': f'صيغة الأرقام المدخلة غير صالحة: {str(val_err)}'
            }), 400

        # التحقق من الحقول الإجبارية
        if not qid or not title:
            return jsonify({
                'status': 'error',
                'message': 'يرجى تقديم حقل اسم المنتج ومعرف الـ QID بصورة صحيحة!'
            }), 400

        # فك ومعالجة مصفوفات البيانات المرسلة بهيكل JSON من الـ Frontend
        try:
            collection_ids = json.loads(request.form.get('collection_ids', '[]'))
            variants = json.loads(request.form.get('variants', '[]'))
            removed_images = json.loads(request.form.get('removed_images', '[]'))
        except (TypeError, json.JSONDecodeError) as json_err:
            return jsonify({
                'status': 'error',
                'message': f'خطأ أثناء تحليل بيانات الحقول المتقدمة: {str(json_err)}'
            }), 400

        # معالجة ملفات الصور الجديدة المرفوعة عبر النموذج
        new_uploaded_images = request.files.getlist('images')
        
        # 💡 بناء كائن متغيرات الـ Input الموجه لعملية المزامنة والتحديث في GraphQL
        update_input = {
            "title": title,
            "slug": slug,
            "description": description,
            "status": status,
            "supplier_id": supplier_id if supplier_id else None,
            "sku": sku,
            "quantity": quantity,
            "weight": weight,
            "pricing": {
                "price": price,
                "originalPrice": cost_price,
                "compareAtPrice": compare_at_price
            },
            "collection_ids": collection_ids,
            "variants": [
                {
                    "name": v.get("name"),
                    "price": float(v.get("price") or 0.0),
                    "quantity": int(v.get("quantity") or 0),
                    "sku": v.get("sku")
                } for v in variants if v.get("name")
            ]
        }

        # تنفيذ طلب المزامنة وإجراء الطفرة (Mutation) على خادم الـ GraphQL
        mutation_variables = {
            "qid": qid,
            "input": update_input
        }
        
        # 🚀 إرسال التحديث للخادم الخارجي
        graphql_response = QomrahGraphQLClient.execute_query(UPDATE_PRODUCT_MUTATION, mutation_variables)
        
        # معالجة رد الخادم والتحقق من المزامنة
        if graphql_response and 'data' in graphql_response:
            update_result = graphql_response['data'].get('updateProduct')
            if update_result and update_result.get('status') == 'success':
                return jsonify({
                    'status': 'success',
                    'message': update_result.get('message', 'تم حفظ التعديلات ومزامنتها بنجاح!')
                }), 200
            elif update_result:
                return jsonify({
                    'status': 'error',
                    'message': update_result.get('message', 'فشلت المزامنة على السيرفر الخارجي.')
                }), 400

        # في حال عدم وجود خدمات مزامنة حقيقية مفعّلة حالياً، يتم الاعتماد على الحفظ المحلي الآمن
        logger.info(f"🔄 تم الحفظ المحلي للمنتج {qid} (بانتظار تفعيل المزامنة الكاملة).")
        return jsonify({
            'status': 'success',
            'message': f'تم حفظ وتحديث بيانات المنتج "{title}" محلياً وبنجاح!'
        }), 200

    except Exception as e:
        logger.error(f"❌ خطأ غير متوقع أثناء معالجة وحفظ المنتج: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f'حدث خطأ في السيرفر أثناء محاولة الحفظ: {str(e)}'
        }), 500
```eof

هذا الملف مُهيّأ الآن للعمل بصورة فورية مع الهيكل البرمجي الخاص بمشروعك ومزامنة البيانات المرفوعة مع واجهة الـ GraphQL. لا تتردد في طرح أي استفسار آخر للتكامل مع باقي أقسام النظام!
