# coding: utf-8
import logging
from flask import render_template, request
from flask_login import login_required
from apps.services.graphql_client import QomrahGraphQLClient
from .registry import admin_product_bp

logger = logging.getLogger(__name__)

@admin_product_bp.route('/', methods=['GET'])
@login_required
def manage_products():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = """
    query Data($input: GetAllProductsInput) {
      findAllProducts(input: $input) {
        data { qid, title, quantity, pricing { price }, images { fileUrl } }
        pagination { totalPages, currentPage, totalItems }
      }
    }
    """
    
    # دمج البحث في المتغيرات بشكل مباشر وأكثر أماناً
    variables = {
        "input": {
            "page": page, 
            "limit": 12, 
            "search": search if search else None
        }
    }
    
    try:
        result = QomrahGraphQLClient.execute_query(query, variables=variables) or {}
    except Exception as e:
        logger.error(f"GraphQL Error: {e}")
        result = {}

    data = result.get('findAllProducts', {})
    products = data.get('data', [])
    pag_info = data.get('pagination', {"totalPages": 1, "currentPage": 1, "totalItems": 0})
    
    # تحسين فئة الترقيم لتسهيل الاستخدام
    class ProPagination:
        def __init__(self, p):
            self.currentPage = p.get('currentPage', 1)
            self.totalPages = p.get('totalPages', 1)
            self.totalItems = p.get('totalItems', 0)
            self.has_prev = self.currentPage > 1
            self.has_next = self.currentPage < self.totalPages
            self.prev_num = self.currentPage - 1
            self.next_num = self.currentPage + 1
            
    return render_template('admin/admin_Product.html', 
                           products=products, 
                           pagination=ProPagination(pag_info),
                           search=search)
