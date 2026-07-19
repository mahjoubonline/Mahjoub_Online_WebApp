# coding: utf-8
# 📂 apps/admin_Product/routes_edit.py

from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from .registry import admin_product_bp
from apps.services.graphql_client import QomrahGraphQLClient
import logging

# محاولة استيراد الموديلات المحلية بشكل آمن لتجنب أي تعطل
try:
    from apps.models.product_supplier_map import ProductSupplierMapping
    from apps.models.supplier import Supplier
    HAS_MODELS = True
except ImportError:
    HAS_MODELS = False

logger = logging.getLogger(__name__)

@admin_product_bp.route('/edit/<path:qid>', methods=['GET'])
@login_required
def edit_product(qid):
    """عرض صفحة تعديل المنتج وجلب البيانات اللازمة للقالب المعتمد"""
    
    # 1. استعلام جلب تفاصيل المنتج الكاملة (بما فيها المتغيرات والمجموعات)
    product_query = """
    query GetProductDetail($qid: ID!) { 
        findProduct(qid: $qid) { 
            qid
            title
            slug
            description
            variants {
                title
                price
                quantity
                sku
            }
            collections {
                qid
            }
        } 
    }
    """
    
    # 2. استعلام جلب المجموعات بالكامل لتغذية خيار الاختيار المتعدد في القالب
    collections_query = """
    query GetAllCollections {
        findAllCollections(input: { limit: 100 }) {
            data {
                qid
                title
            }
        }
    }
    """

    try:
        # تنفيذ الاستعلامات في قمرة
        prod_response = QomrahGraphQLClient.execute_query(product_query, {"qid": qid})
        col_response = QomrahGraphQLClient.execute_query(collections_query)
        
        if not prod_response or 'data' not in prod_response or not prod_response['data'].get('findProduct'):
            flash("❌ تعذر جلب بيانات المنتج من منصة قمرة.")
            return redirect(url_for('admin_product_bp.manage_products'))
            
        product = prod_response['data']['findProduct']
        
        # تحويل صيغة المجموعات لتتوافق مع شرط القالب (col.qid in product.collection_ids)
        product['collection_ids'] = [c['qid'] for c in product.get('collections', []) if c]
        
        # جلب قائمة المجموعات الكاملة من قمرة
        all_collections = []
        if col_response and 'data' in col_response and col_response['data'].get('findAllCollections'):
            all_collections = col_response['data']['findAllCollections'].get('data', [])

        # 3. جلب بيانات الموردين والربط الحالي من قاعدة البيانات المحلية
        suppliers = []
        mapping_data = {"selected_supplier_id": None}
        
        if HAS_MODELS:
            try:
                suppliers = Supplier.query.all()
                mapping = ProductSupplierMapping.query.filter_by(product_qid=qid).first()
                if mapping:
                    mapping_data["selected_supplier_id"] = mapping.supplier_id
            except Exception as db_err:
                logger.error(f"⚠️ خطأ أثناء جلب الموردين محلياً: {db_err}")

        # تمرير كافة البيانات المتوافقة مع بنية القالب الجديد
        return render_template(
            'admin/admin_edit_product.html', 
            product=product, 
            suppliers=suppliers, 
            mapping=mapping_data, 
            all_collections=all_collections
        )

    except Exception as e:
        logger.error(f"❌ خطأ غير متوقع في موديول التعديل: {str(e)}")
        flash("حدث خطأ تقني أثناء تحميل الصفحة.")
        return redirect(url_for('admin_product_bp.manage_products'))
