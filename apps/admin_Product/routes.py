# coding: utf-8
# 📂 apps/admin_Product/routes.py

import logging
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from apps.services.graphql_client import QomrahGraphQLClient
from apps.api.sync_engine import ProductSyncEngine
from apps.models.product_db import Product

logger = logging.getLogger(__name__)
admin_product_bp = Blueprint('admin_product_bp', __name__, template_folder='templates')

@admin_product_bp.app_context_processor
def inject_utils():
    return dict(max=max, min=min)

@admin_product_bp.route('/', methods=['GET'])
@login_required
def manage_products():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    # 1. إذا كان هناك بحث: نبحث في قاعدة البيانات المحلية (البحث الشامل)
    if search:
        pagination = Product.query.filter(Product.title.ilike(f'%{search}%')).paginate(page=page, per_page=20, error_out=False)
        return render_template('admin/admin_Product.html', 
                               products=pagination.items, 
                               pagination=pagination)

    # 2. إذا لم يكن هناك بحث: نجلب البيانات من الـ API (عرض افتراضي)
    query = """
    query Data($input: GetAllProductsInput) {
      findAllProducts(input: $input) {
        data { qid, title, quantity, pricing { price }, images { fileUrl }, identification { sku } }
        pagination { totalPages, currentPage, totalItems }
      }
    }
    """
    variables = {"input": {"page": page, "limit": 20}} # تمت إزالة search هنا لتجنب الخطأ
    
    try:
        result = QomrahGraphQLClient.execute_query(query, variables=variables)
    except Exception as e:
        logger.error(f"GraphQL Error: {e}")
        result = {}
    
    data = result.get('findAllProducts', {}) if result else {}
    products = data.get('data', [])
    pag_info = data.get('pagination', {"totalPages": 1, "currentPage": 1, "totalItems": 0})
    
    # تحويل بيانات الـ API لنمط يدعم الترقيم (محاكاة)
    class MockPagination:
        def __init__(self, p):
            self.page = p['currentPage']
            self.pages = p['totalPages']
            self.has_prev = lambda: self.page > 1
            self.has_next = lambda: self.page < self.pages
            self.prev_num = lambda: self.page - 1
            self.next_num = lambda: self.page + 1
            self.total = p['totalItems']
            
    return render_template('admin/admin_Product.html', 
                           products=products, 
                           pagination=MockPagination(pag_info))

@admin_product_bp.route('/proxy-sync', methods=['POST'])
@login_required
def proxy_sync():
    total_synced = 0
    page = 1
    try:
        while True:
            query = """
            query Data($input: GetAllProductsInput) {
              findAllProducts(input: $input) {
                data { qid, title, quantity, pricing { price }, identification { sku }, images { fileUrl } }
                pagination { hasNextPage }
              }
            }
            """
            result = QomrahGraphQLClient.execute_query(query, variables={"input": {"page": page, "limit": 50}})
            if not result or 'findAllProducts' not in result: break
            products_data = result['findAllProducts'].get('data', [])
            if not products_data: break
            total_synced += ProductSyncEngine.process_products(products_data)
            if not result['findAllProducts'].get('pagination', {}).get('hasNextPage'):
                break
            page += 1
        return jsonify({"status": "success", "message": f"تمت المزامنة بنجاح: تم تحديث {total_synced} منتج."})
    except Exception as e:
        logger.error(f"Sync Error: {e}")
        return jsonify({"status": "error", "message": "حدث خطأ أثناء مزامنة البيانات"}), 500

@admin_product_bp.route('/add', methods=['GET'])
@login_required
def add_product():
    return render_template('admin/admin_add_product.html', product=None)

@admin_product_bp.route('/edit/<qid>', methods=['GET'])
@login_required
def edit_product(qid):
    product = Product.query.filter_by(qid=qid).first()
    return render_template('admin/admin_add_product.html', product=product)

@admin_product_bp.route('/save-sync', methods=['POST'])
@login_required
def save_sync():
    return jsonify({"status": "success", "message": "تم التخطي"})
