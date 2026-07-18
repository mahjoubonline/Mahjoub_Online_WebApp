# coding: utf-8
# 📂 apps/admin_Product/routes_sync.py

from flask import request, jsonify
from flask_login import login_required
from .registry import admin_product_bp
from apps.services.graphql_client import QomrahGraphQLClient
import logging

logger = logging.getLogger(__name__)

@admin_product_bp.route('/save-sync', methods=['POST'])
@login_required
def save_sync():
    """
    مسار لحفظ بيانات منتج محدد وإرسال التحديثات إلى منصة قمرة
    """
    data = request.get_json()
    if not data or 'qid' not in data:
        return jsonify({"status": "error", "message": "بيانات غير صالحة"}), 400

    try:
        # بناءً على هيكل قمرة، التحديث يتم عبر Mutation مخصص للمعلومات
        mutation = """
        mutation UpdateProductInfo($id: String!, $input: UpdateProductInfoInput!) {
            updateProductInfo(id: $id, input: $input) {
                qid
                title
            }
        }
        """
        
        # تجهيز المدخلات حسب الـ Schema المتوقعة
        variables = {
            "id": data['qid'],
            "input": {
                "title": data.get('title'),
                "quantity": int(data.get('quantity', 0))
                # ملاحظة: إذا كان الـ Schema يدعم السعر أو SKU في التحديث، 
                # أضفهما هنا بنفس النمط: "price": float(data.get('price', 0))
            }
        }
        
        # تنفيذ الاستعلام عبر عميل GraphQL
        response = QomrahGraphQLClient.execute_query(mutation, variables=variables)
        
        # التحقق من استجابة الـ GraphQL
        if not response or 'errors' in response:
            error_msg = response.get('errors', 'فشل غير معروف')
            logger.error(f"❌ خطأ من قمرة: {error_msg}")
            return jsonify({"status": "error", "message": "فشلت عملية التحديث في قمرة"}), 400
        
        logger.info(f"✅ تم تحديث المنتج بنجاح: {data.get('qid')}")
        return jsonify({
            "status": "success", 
            "message": "تم تحديث البيانات بنجاح في قمرة"
        }), 200
        
    except Exception as e:
        logger.error(f"❌ خطأ داخلي أثناء الحفظ: {str(e)}")
        return jsonify({"status": "error", "message": f"حدث خطأ داخلي: {str(e)}"}), 500
