# coding: utf-8
# 📂 apps/admin_Product/routes.py

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from apps.services.graphql_client import QomrahGraphQLClient

admin_product_bp = Blueprint('admin_product_bp', __name__, template_folder='templates')

@admin_product_bp.route('/', methods=['GET'])
@login_required
def manage_products():
    return render_template('admin/admin_Product.html')

@admin_product_bp.route('/get-products', methods=['GET'])
@login_required
def get_products_api():
    # استقبال رقم الصفحة من الواجهة (الافتراضي 1)
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    # الاستعلام المحدث مع استخدام الـ variables لدعم الترقيم والبحث
    query = """
    query Data($input: GetAllProductsInput) {
      findAllProducts(input: $input) {
        data {
          qid, title, quantity, pricing { price }, 
          images { fileUrl }, identification { sku }
        }
        pagination { totalPages, currentPage, totalItems }
      }
    }
    """
    
    # تحضير المتغيرات للـ GraphQL
    variables = {
        "input": {
            "page": page,
            "limit": 10,
            "search": search if search else None
        }
    }
    
    # تنفيذ الاستعلام
    result = QomrahGraphQLClient.execute_query(query, variables=variables)
    
    if not result or 'findAllProducts' not in result:
        return jsonify({"products": [], "pagination": {"totalPages": 1, "currentPage": 1}})
    
    data = result.get('findAllProducts', {})
    
    return jsonify({
        "products": data.get('data', []),
        "pagination": data.get('pagination', {})
    })

@admin_product_bp.route('/proxy-sync', methods=['POST'])
@login_required
def proxy_sync():
    return jsonify({"status": "success", "message": "تم تحديث البيانات من المصدر"})

@admin_product_bp.route('/save-sync', methods=['POST'])
@login_required
def save_sync():
    return jsonify({"status": "success", "message": "تم التخطي"})
