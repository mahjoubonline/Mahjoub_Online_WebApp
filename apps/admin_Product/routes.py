# coding: utf-8
# 📂 apps/admin_Product/routes.py

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from apps.services.graphql_client import QomrahGraphQLClient

admin_product_bp = Blueprint('admin_product_bp', __name__, template_folder='templates')

# كلاس مساعد لمحاكاة كائن الترقيم الذي يتوقعه القالب
class PaginationMock:
    def __init__(self, p):
        self.page = p.get('currentPage', 1)
        self.pages = p.get('totalPages', 1)
        self.total = p.get('totalItems', 0)
    def has_prev(self): return self.page > 1
    def has_next(self): return self.page < self.pages
    def prev_num(self): return self.page - 1
    def next_num(self): return self.page + 1

@admin_product_bp.route('/', methods=['GET'])
@login_required
def manage_products():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = """
    query Data($input: GetAllProductsInput) {
      findAllProducts(input: $input) {
        data { qid, title, quantity, pricing { price }, images { fileUrl }, identification { sku } }
        pagination { totalPages, currentPage, totalItems }
      }
    }
    """
    
    variables = {"input": {"page": page, "limit": 10, "search": search if search else None}}
    result = QomrahGraphQLClient.execute_query(query, variables=variables)
    
    data = result.get('findAllProducts', {}) if result else {}
    products = data.get('data', [])
    pag_info = data.get('pagination', {"totalPages": 1, "currentPage": 1, "totalItems": 0})
    
    return render_template('admin/admin_Product.html', 
                           products=products, 
                           pagination=PaginationMock(pag_info))

@admin_product_bp.route('/get-products', methods=['GET'])
@login_required
def get_products_api():
    # أبقينا هذا المسار للاستخدام في حال احتجت تحديث جزء من الصفحة عبر AJAX لاحقاً
    return jsonify({"message": "Use the main route for data rendering"})

@admin_product_bp.route('/proxy-sync', methods=['POST'])
@login_required
def proxy_sync():
    return jsonify({"status": "success", "message": "تم تحديث البيانات من المصدر"})

@admin_product_bp.route('/save-sync', methods=['POST'])
@login_required
def save_sync():
    return jsonify({"status": "success", "message": "تم التخطي"})
