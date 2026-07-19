# coding: utf-8
# 📂 apps/admin_Product/routes_sync.py

from flask import request, jsonify
from .registry import admin_product_bp
from apps.services.graphql_client import QomrahGraphQLClient
import logging

try:
    from apps.models.product_supplier_map import ProductSupplierMapping
    from apps.extensions import db
    HAS_DB = True
except ImportError:
    HAS_DB = False

logger = logging.getLogger(__name__)

@admin_product_bp.route('/save-sync', methods=['POST'])
def save_sync():
    """مزامنة بيانات المنتج (بما فيها المخزون والشحن) مع منصة قمرة وحفظ المورد محلياً"""
    data = request.json or {}
    qid = data.get('qid')
    supplier_id = data.get('supplier_id')
    
    if not qid:
        return jsonify({"status": "error", "message": "المعرف الفريد QID مفقود"}), 400

    # 1. معالجة البيانات القادمة من القالب
    try:
        # معالجة المتغيرات
        raw_variants = data.get('variants', [])
        processed_variants = []
        for v in raw_variants:
            processed_variants.append({
                "pricing": {"price": float(v.get('price', 0))},
                "quantity": int(v.get('quantity', 0)),
                "sku": v.get('sku', '')
            })
        
    except (ValueError, TypeError) as e:
        return jsonify({"status": "error", "message": f"خطأ في تنسيق البيانات: {str(e)}"}), 400

    # 2. صياغة الـ Mutation المحدث
    mutation = """
    mutation UpdateProduct($qid: String!, $input: UpdateProductInput!) {
        updateProduct(qid: $qid, input: $input) {
            success
            message
        }
    }
    """
    
    # 3. بناء الـ Variables مع الحقول الجديدة (الوزن، SKU، والأسعار)
    variables = {
        "qid": qid,
        "input": {
            "title": data.get('title'),
            "slug": data.get('slug'),
            "description": data.get('description'),
            "status": data.get('status'),
            "sku": data.get('sku'),
            "quantity": int(data.get('quantity', 0)),
            "weight": float(data.get('weight', 0)),
            "pricing": {
                "price": float(data.get('price', 0)),
                "compareAtPrice": float(data.get('compare_at_price', 0)),
                "originalPrice": float(data.get('original_price', 0))
            },
            "collectionIds": data.get('collection_ids', []),
            "variants": processed_variants,
            "images": [{"fileUrl": url} for url in data.get('images', [])]
        }
    }
    
    try:
        # إرسال التحديث إلى منصة قمرة
        qomrah_response = QomrahGraphQLClient.execute_query(mutation, variables)
        
        if not qomrah_response or 'errors' in qomrah_response:
            error_msg = qomrah_response.get('errors', [{}])[0].get('message', 'خطأ غير معروف')
            return jsonify({"status": "error", "message": f"فشل التحديث في قمرة: {error_msg}"}), 500

        # 4. تحديث ربط المورد محلياً
        if HAS_DB:
            try:
                mapping = ProductSupplierMapping.query.filter_by(product_qid=qid).first()
                if supplier_id: 
                    if mapping:
                        mapping.supplier_id = supplier_id
                    else:
                        new_mapping = ProductSupplierMapping(product_qid=qid, supplier_id=supplier_id)
                        db.session.add(new_mapping)
                else: 
                    if mapping:
                        db.session.delete(mapping)
                
                db.session.commit()
            except Exception as db_err:
                db.session.rollback()
                logger.error(f"⚠️ فشل حفظ المورد: {str(db_err)}")
                return jsonify({"status": "warning", "message": "تم تحديث المنتج في قمرة، لكن فشل حفظ المورد محلياً"})

        return jsonify({"status": "success", "message": "✅ تم حفظ التعديلات بنجاح!"})

    except Exception as e:
        logger.error(f"❌ خطأ برمي: {str(e)}")
        return jsonify({"status": "error", "message": "حدث خطأ غير متوقع أثناء المعالجة"}), 500
