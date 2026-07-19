# coding: utf-8
# 📂 apps/admin_Product/routes_sync.py

from flask import request, jsonify
from flask_login import login_required
from .registry import admin_product_bp
from apps.services.graphql_client import QomrahGraphQLClient
from apps.models import db
from apps.models.product_supplier_map import ProductSupplierMapping
import logging

logger = logging.getLogger(__name__)

@admin_product_bp.route('/save-sync', methods=['POST'])
@login_required
def save_sync():
    """
    حفظ بيانات المنتج وتحديثها في قمرة وقاعدة البيانات المحلية (تحديث متزامن)
    """
    data = request.get_json()
    
    if not data or 'qid' not in data:
        return jsonify({"status": "error", "message": "معرف المنتج مفقود"}), 400

    try:
        # 1. تحديث الربط والملاحظات في قاعدة البيانات المحلية (MySQL)
        mapping = ProductSupplierMapping.query.filter_by(product_qid=data['qid']).first()
        
        # تحويل القيمة الفارغة لـ supplier_id إلى None
        supplier_id = data.get('supplier_id')
        if supplier_id == "":
            supplier_id = None
            
        if mapping:
            mapping.supplier_id = supplier_id
            mapping.internal_notes = data.get('internal_notes', '') 
        else:
            new_mapping = ProductSupplierMapping(
                product_qid=data['qid'], 
                supplier_id=supplier_id,
                internal_notes=data.get('internal_notes', '')
            )
            db.session.add(new_mapping)
        
        db.session.commit()

        # 2. بناء الـ Mutation المحدث (لقمرة)
        mutation = """
        mutation UpdateProductInfo($id: String!, $input: UpdateProductInfoInput!) {
            updateProductInfo(id: $id, input: $input) {
                qid
                title
            }
        }
        """
        
        # 3. تجهيز المدخلات
        variables = {
            "id": str(data['qid']),
            "input": {
                "title": str(data.get('title', '')),
                "slug": str(data.get('slug', '')),
                "quantity": int(data.get('quantity', 0)),
                "pricing": {
                    "price": float(data.get('price', 0))
                },
                "identification": {
                    "sku": str(data.get('sku', ''))
                }
            }
        }
        
        # 4. تنفيذ التحديث في قمرة
        response = QomrahGraphQLClient.execute_query(mutation, variables=variables)
        
        if not response or 'errors' in response:
            logger.error(f"❌ فشل تحديث قمرة لـ {data['qid']}: {response.get('errors')}")
            # التحديث المحلي تم، لذا نبلغ المستخدم بالحالة الجزئية
            return jsonify({"status": "partial_success", "message": "تم حفظ الملاحظات محلياً، لكن فشل التحديث في قمرة"}), 500
        
        return jsonify({"status": "success", "message": "تم حفظ كافة التعديلات بنجاح في النظامين"}), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ خطأ تقني أثناء عملية المزامنة للـ qid {data.get('qid')}: {str(e)}")
        return jsonify({"status": "error", "message": "حدث خطأ داخلي أثناء حفظ البيانات"}), 500
