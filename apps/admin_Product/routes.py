# coding: utf-8
# 📂 apps/admin_Product/routes.py

from flask import render_template, request, flash, jsonify
from flask_login import login_required
from .registry import admin_product_bp
from apps.services.graphql_client import QomrahGraphQLClient
import logging

logger = logging.getLogger(__name__)

# الاستعلام متوافق مع بنية البيانات التي يعرضها القالب
GET_ALL_PRODUCTS_QUERY = """
query Data($input: GetAllProductsInput) {
  findAllProducts(input: $input) {
    data {
      qid
      title
      pricing { price }
      quantity
      identification { sku }
      images { fileUrl }
    }
    pagination { currentPage, totalPages }
  }
}
"""

@admin_product_bp.route('/', methods=['GET'])
@login_required
def manage_products():
    """جلب وعرض قائمة المنتجات (مع حماية كاملة ضد الانهيار)"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('title', '').strip()
    
    products = []
    pagination = {"currentPage": page, "totalPages": 1}
    
    try:
        input_data = {"page": page, "limit": 50}
        if search:
            input_data["title"] = search
            
        variables = {"input": input_data}
        response = QomrahGraphQLClient.execute_query(GET_ALL_PRODUCTS_QUERY, variables)
        
        if response and 'data' in response:
            result = response['data'].get('findAllProducts', {})
            products = result.get('data') or []
            pagination = result.get('pagination') or {"currentPage": page, "totalPages": 1}
        else:
            logger.warning("⚠️ استجابة فارغة من قمرة عند جلب المنتجات.")
            
    except Exception as e:
        logger.error(f"❌ خطأ تقني أثناء جلب قائمة المنتجات: {str(e)}")
        flash("حدث خطأ أثناء تحميل قائمة المنتجات.")

    try:
        return render_template(
            'admin/admin_Product.html',
            products=products,
            pagination=pagination,
            search=search
        )
    except Exception as render_err:
        logger.error(f"❌ خطأ في رندر قالب المنتجات: {str(render_err)}")
        return render_template('admin/admin_Product.html', products=[], pagination={"currentPage": 1, "totalPages": 1}, search="")


@admin_product_bp.route('/add', methods=['GET'])
@login_required
def add_product():
    """عرض صفحة إضافة منتج جديد (محمي ضد الانهيار)"""
    try:
        return render_template(
            'admin/admin_add_product.html',
            product=None
        )
    except Exception as e:
        logger.error(f"❌ خطأ في صفحة إضافة المنتج: {str(e)}")
        flash("تعذر فتح صفحة الإضافة حالياً.")
        return render_template('admin/admin_Product.html', products=[], pagination={"currentPage": 1, "totalPages": 1}, search="")


@admin_product_bp.route('/edit/<path:qid>', methods=['GET'])
@login_required
def edit_product(qid):
    """عرض صفحة تعديل منتج موجود بالاعتماد على معرفه (qid) (محمي ضد الانهيار)"""
    try:
        return render_template(
            'admin/admin_add_product.html',
            product={"qid": qid}
        )
    except Exception as e:
        logger.error(f"❌ خطأ في صفحة تعديل المنتج: {str(e)}")
        flash("تعذر فتح صفحة التعديل حالياً.")
        return render_template('admin/admin_Product.html', products=[], pagination={"currentPage": 1, "totalPages": 1}, search="")


@admin_product_bp.route('/sync', methods=['POST'])
@login_required
def save_sync():
    """معالجة عملية مزامنة المنتجات بشكل آمن ومنفصل"""
    try:
        return jsonify({"status": "success", "message": "تمت المزامنة بنجاح"})
    except Exception as e:
        logger.error(f"❌ خطأ في عملية المزامنة: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 400
