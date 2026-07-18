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
    # استقبال المتغيرات
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').strip()
    
    # استعلام GraphQL مع دعم البحث عبر حقل 'title'
    query = """
    query Data($input: GetAllProductsInput) {
      findAllProducts(input: $input) {
        data { qid, title, quantity, pricing { price }, images { fileUrl } }
        pagination { totalPages, currentPage, totalItems }
      }
    }
    """
    
    # منطق البحث: إذا وُجد نص بحث، نرسله إلى 'title' في الـ Schema
    variables = {
        "input": {
            "page": page, 
            "limit": 50, 
            "title": search if search else None
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
    
    # كلاس الترقيم
    class ProPagination:
        def __init__(self, p):
            self.currentPage = p.get('currentPage', 1)
            self.totalPages = p.get('totalPages', 1)
            self.totalItems = p.get('totalItems', 0)
            
    return render_template('admin/admin_Product.html', 
                           products=products, 
                           pagination=ProPagination(pag_info),
                           search=search)
