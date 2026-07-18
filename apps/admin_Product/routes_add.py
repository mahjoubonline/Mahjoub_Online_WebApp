# coding: utf-8
# 📂 apps/admin_Product/routes_add.py

from flask import render_template, request, jsonify
from flask_login import login_required
# ✅ الاستيراد الصحيح المباشر والآمن لمنع أي تعارض دائري أثناء الإقلاع
from .registry import admin_product_bp
from apps.services.graphql_client import QomrahGraphQLClient
import logging

logger = logging.getLogger(__name__)

@admin_product_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    """
    صفحة إضافة منتج جديد لمتجر محجوب أونلاين.
    - في حالة GET: عرض نموذج الإضافة الأنيق (باللونين الأبيض والأرجواني).
    - في حالة POST: معالجة البيانات وإرسالها إلى سيرفر منصة قمرة.
    """
    if request.method == 'GET':
        return render_template('admin/add_product.html')

    # معالجة طلبات الإضافة عبر الـ POST
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "لم يتم استقبال بيانات صالحة"}), 400

    # 🚀 هيكل الـ Mutation المخصص لإنشاء منتج جديد في منصة قمرة
    mutation = """
    mutation CreateProduct($input: CreateProductInput!) {
        createProduct(input: $input) {
            status
            message
            product {
                qid
                title
            }
        }
    }
    """

    try:
        # إرسال البيانات المجمعة من الواجهة إلى سيرفر GraphQL
        result = QomrahGraphQLClient.execute_query(mutation, variables={"input": data}) or {}
        response_data = result.get('createProduct', {})

        if response_data.get('status') == 'success' or 'product' in response_data:
            product_info = response_data.get('product', {})
            logger.info(f"✅ تم إنشاء المنتج بنجاح في قمرة بمعرف: {product_info.get('qid')}")
            return jsonify({
                "status": "success", 
                "message": "تمت إضافة المنتج ومزامنته مع قمرة بنجاح"
            }), 200
        else:
            return jsonify({
                "status": "error", 
                "message": response_data.get('message', 'فشلت عملية إضافة المنتج في السيرفر الرئيسي')
            }), 400

    except Exception as e:
        logger.error(f"❌ خطأ غير متوقع أثناء إضافة منتج جديد: {e}")
        return jsonify({"status": "error", "message": "حدث خطأ داخلي في الخادم أثناء المعالجة."}), 500
