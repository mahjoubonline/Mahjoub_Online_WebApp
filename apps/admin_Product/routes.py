# coding: utf-8
# 📂 apps/admin_Product/routes.py

from flask import render_template, request, flash
from flask_login import login_required
from .registry import admin_product_bp
from apps.services.graphql_client import QomrahGraphQLClient
import logging

logger = logging.getLogger(__name__)

# استعلام جلب كل المنتجات
GET_ALL_PRODUCTS_QUERY = """
query Data($input: GetAllProductsInput) {
  findAllProducts(input: $input) {
    data {
      qid
      title
      pricing { price }
      quantity
      images { fileUrl }
    }
    pagination { currentPage, totalPages }
  }
}
"""

# استعلام جلب تفاصيل منتج واحد للتعديل
GET_PRODUCT_BY_ID_QUERY = """
query Data($qid: ID!) {
  findProductById(qid: $qid) {
    qid
    title
    pricing { price }
    quantity
    images { fileUrl }
  }
}
"""

@admin_product_bp.route('/', methods=['GET'])
@login_required
def manage_products():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('title', '').strip()
    
    input_data = {"page": page, "limit": 50}
    if search:
        input_data["title"] = search
        
    variables = {"input": input_data}
    
    products = []
    pagination = {"currentPage": page, "totalPages": 1}
    
    try:
        response = QomrahGraphQLClient.execute_query(GET_ALL_PRODUCTS_QUERY, variables)
        
        if response:
            root = response.get('data', response)
            result = root.get('findAllProducts', {})
            products = result.get('data') if result.get('data') is not None else []
            pagination = result.get('pagination') or {"currentPage": page, "totalPages": 1}
            
    except Exception as e:
        logger.error(f"❌ خطأ أثناء جلب البيانات: {e}")
        flash("حدث خطأ أثناء تحميل قائمة المنتجات.")

    return render_template(
        'admin/admin_Product.html',
        products=products,
        pagination=pagination,
        search=search
    )

@admin_product_bp.route('/edit/<qid>', methods=['GET'])
@login_required
def edit_product(qid):
    """جلب بيانات المنتج من قمرة وعرضها في صفحة التعديل"""
    try:
        variables = {"qid": qid}
        response = QomrahGraphQLClient.execute_query(GET_PRODUCT_BY_ID_QUERY, variables)
        
        product = {}
        if response and 'data' in response and response['data'].get('findProductById'):
            product = response['data']['findProductById']
        else:
            flash("لم يتم العثور على المنتج في قمرة.")
            
        return render_template('admin/admin_edit_product.html', product=product)
        
    except Exception as e:
        logger.error(f"❌ خطأ في جلب تفاصيل المنتج {qid}: {e}")
        flash("حدث خطأ أثناء تحميل بيانات المنتج للتعديل.")
        return render_template('admin/admin_edit_product.html', product={})
