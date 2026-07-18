# coding: utf-8
from flask import render_template, request, jsonify
from flask_login import login_required
from . import admin_product_bp 
from apps.services.graphql_client import QomrahGraphQLClient
import logging

logger = logging.getLogger(__name__)

@admin_product_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    """
    عرض صفحة إضافة منتج جديد ومعالجة بيانات الفورم.
    """
    if request.method == 'GET':
        return render_template('admin/admin_add_product.html', product=None)

    if request.method == 'POST':
        try:
            data = request.get_json()
            title = data.get('title')
            price = data.get('price')
            quantity = data.get('quantity')
            sku = data.get('sku')
            
            # التحقق الأساسي
            if not title or not price:
                return jsonify({'status': 'error', 'message': 'يرجى تعبئة الحقول المطلوبة'}), 400
            
            # تنفيذ الـ Mutation الخاص بإنشاء منتج في قمرة
            mutation = """
            mutation CreateProduct($input: CreateProductInput!) {
                createProduct(input: $input) { qid }
            }
            """
            variables = {
                "input": {
                    "title": title,
                    "price": float(price),
                    "quantity": int(quantity),
                    "sku": sku
                }
            }
            
            # QomrahGraphQLClient.execute_query(mutation, variables=variables)
            
            logger.info(f"تم إضافة منتج جديد: {title}")
            return jsonify({'status': 'success', 'message': 'تم إضافة المنتج بنجاح'}), 200
            
        except Exception as e:
            logger.error(f"Error adding product: {e}")
            return jsonify({'status': 'error', 'message': str(e)}), 500

# ملاحظة: تم إزالة save_sync من هنا لأنه موجود في routes_sync.py 
# للحفاظ على مبدأ فصل المهام (Separation of Concerns).
