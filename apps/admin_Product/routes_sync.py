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
    """استقبل بيانات التعديل الكاملة من القالب، مزامنتها مع قمرة، وحفظ المورد محلياً"""
    data = request.json or {}
    qid = data.get('qid')
    supplier_id = data.get('supplier_id')
    
    if not qid:
        return jsonify({"status": "error", "message": "المعرف الفريد QID مفقود"}), 400

    # 1. صياغة الـ Mutation لتحديث المنتج في قمرة بكامل بيانات القالب الجديد
    mutation = """
    mutation UpdateProductFromHub($qid: ID!, $input: UpdateProductInput!) {
        updateProduct(qid: $qid, input: $input) {
            qid
        }
    }
    """
    
    # بناء المتغيرات بالشكل الذي يقبله الـ API لتحديث المجموعات والمتغيرات والوصف
    variables = {
        "qid": qid,
        "input": {
            "title": data.get('title'),
            "slug": data.get('slug'),
            "description": data.get('description'),
            "collectionIds": data.get('collection_ids', []),
            "variants": data.get('variants', [])
        }
    }
    
    try:
        # إرسال التحديث لحظياً إلى منصة قمرة
        qomrah_response = QomrahGraphQLClient.execute_query(mutation, variables)
        
        if not qomrah_response or 'errors' in qomrah_response:
            logger.error(f"❌ خطأ من API قمرة: {qomrah_response.get('errors') if qomrah_response else 'لا توجد استجابة'}")
            return jsonify({"status": "error", "message": "فشل تحديث البيانات في منصة قمرة"}), 500

        # 2. تحديث ربط المورد في قاعدة البيانات المحلية (إذا كانت مهيأة)
        if HAS_DB and supplier_id:
            try:
                mapping = ProductSupplierMapping.query.filter_by(product_qid=qid).first()
                if mapping:
                    mapping.supplier_id = supplier_id
                else:
                    new_mapping = ProductSupplierMapping(product_qid=qid, supplier_id=supplier_id)
                    db.session.add(new_mapping)
                db.session.commit()
            except Exception as db_err:
                db.session.rollback()
                logger.error(f"⚠️ تم التحديث في قمرة ولكن فشل حفظ المورد محلياً: {str(db_err)}")
                return jsonify({"status": "success", "message": "تم حفظ المنتج في قمرة، لكن فشل تحديث المورد محلياً"})

        return jsonify({"status": "success", "message": "✅ تم حفظ وتحديث كافة البيانات بنجاح في قمرة والنظام المحلي!"})

    except Exception as e:
        logger.error(f"❌ خطأ برمي أثناء المزامنة: {str(e)}")
        return jsonify({"status": "error", "message": "حدث خطأ غير متوقع أثناء معالجة الطلب"}), 500
