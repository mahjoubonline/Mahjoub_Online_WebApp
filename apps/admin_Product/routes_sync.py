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
    
    # 1. التحقق الأساسي من وجود البيانات
    if not data or 'qid' not in data:
        return jsonify({"status": "error", "message": "بيانات غير صالحة: معرف المنتج مفقود"}), 400

    try:
        # 2. بناء الـ Mutation لتحديث بيانات المنتج
        mutation = """
        mutation UpdateProductInfo($id: String!, $input: UpdateProductInfoInput!) {
            updateProductInfo(id: $id, input: $input) {
                qid
                title
            }
        }
        """
        
        # 3. تجهيز المدخلات (تأكد من مطابقة أسماء الحقول لما يقبله الـ Schema في قمرة)
        # نقوم بتحويل البيانات لأنواعها الصحيحة قبل الإرسال
        variables = {
            "id": str(data['qid']),
            "input": {
                "title": str(data.get('title', '')),
                "quantity": int(data.get('quantity', 0))
                # إذا كنت تريد إضافة دعم السعر لاحقاً، أضف السطر التالي:
                # "price": float(data.get('price', 0.0))
            }
        }
        
        # 4. تنفيذ الاستعلام عبر عميل GraphQL
        response = QomrahGraphQLClient.execute_query(mutation, variables=variables)
        
        # 5. معالجة الاستجابة
        if not response:
            logger.error(f"❌ استجابة فارغة من قمرة عند محاولة تحديث المنتج: {data['qid']}")
            return jsonify({"status": "error", "message": "لا يوجد اتصال بخادم قمرة"}), 503

        if 'errors' in response:
            error_msg = response.get('errors', 'خطأ غير محدد')
            logger.error(f"❌ خطأ من قمرة أثناء تحديث المنتج {data['qid']}: {error_msg}")
            return jsonify({"status": "error", "message": "فشلت عملية التحديث في قمرة"}), 400
        
        logger.info(f"✅ تم تحديث المنتج بنجاح في قمرة: {data.get('qid')}")
        return jsonify({
            "status": "success", 
            "message": "تم تحديث البيانات بنجاح في قمرة"
        }), 200
        
    except ValueError as ve:
        logger.error(f"❌ خطأ في تنسيق البيانات للمنتج {data.get('qid')}: {str(ve)}")
        return jsonify({"status": "error", "message": "بيانات المنتج غير صحيحة"}), 400
        
    except Exception as e:
        logger.error(f"❌ خطأ داخلي أثناء الحفظ في المنتج {data.get('qid')}: {str(e)}")
        return jsonify({"status": "error", "message": "حدث خطأ داخلي غير متوقع"}), 500
