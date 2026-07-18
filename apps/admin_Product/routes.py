# coding: utf-8
import logging
from flask import render_template, request
from flask_login import login_required
from apps.services.graphql_client import QomrahGraphQLClient
# نقوم باستيراد الـ Blueprint من ملف الـ registry لتجنب الحلقات المفرغة
from .registry import admin_product_bp

logger = logging.getLogger(__name__)

@admin_product_bp.route('/', methods=['GET'])
@login_required
def manage_products():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    # تحسين الاستعلام ليشمل الترقيم والبحث
    query = """
    query Data($input: GetAllProductsInput) {
      findAllProducts(input: $input) {
        data { qid, title, quantity, pricing { price }, images { fileUrl } }
        pagination { totalPages, currentPage, totalItems }
      }
    }
    """
    
    # منطق المتغيرات للبحث
    variables = {"input": {"page": page, "limit": 20, "search": search} if search else {"page": page, "limit": 20}}
    
    try:
        result = QomrahGraphQLClient.execute_query(query, variables=variables) or {}
    except Exception as e:
        logger.error(f"GraphQL Error: {e}")
        result = {}

    data = result.get('findAllProducts', {})
    products = data.get('data', [])
    pag_info = data.get('pagination', {"totalPages": 1, "currentPage": 1, "totalItems": 0})
    
    # فئة مساعدة لتسهيل التعامل مع الترقيم في الـ Jinja2
    class ProPagination:
        def __init__(self, p):
            self.currentPage = p['currentPage']
            self.totalPages = p['totalPages']
            self.totalItems = p['totalItems']
            self.page = p['currentPage']
            self.pages = p['totalPages']
            self.total = p['totalItems']
            self.has_prev = lambda: self.page > 1
            self.has_next = lambda: self.page < self.pages
            self.prev_num = lambda: self.page - 1
            self.next_num = lambda: self.page + 1
            
    return render_template('admin/admin_Product.html', 
                           products=products, 
                           pagination=ProPagination(pag_info),
                           search=search)
