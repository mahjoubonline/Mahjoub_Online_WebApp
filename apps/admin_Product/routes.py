# coding: utf-8
# 📂 apps/admin_Product/routes.py

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from apps.services.graphql_client import QomrahGraphQLClient
import math

admin_product_bp = Blueprint('admin_product_bp', __name__, template_folder='templates')

@admin_product_bp.route('/', methods=['GET'])
@login_required
def manage_products():
    return render_template('admin/admin_Product.html')

@admin_product_bp.route('/get-products', methods=['GET'])
@login_required
def get_products_api():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').lower()
    per_page = 10
    
    query = """
    query Data {
      findAllProducts(input: { limit: 99999 }) {
        data {
          qid, title, quantity, pricing { price }, 
          images { fileUrl }, identification { sku }
        }
      }
    }
    """
    
    result = QomrahGraphQLClient.execute_query(query)
    
    # --- إضافة تشخيص للأخطاء ---
    if result is None:
        print("DEBUG: GraphQL returned None")
    else:
        print(f"DEBUG: GraphQL returned: {result.keys()}")
    
    all_products = result.get('findAllProducts', {}).get('data', []) if result else []
    
    # إذا كانت القائمة فارغة، نطبع السجل للتأكد
    if not all_products:
        print(f"DEBUG: No products found. Full result: {result}")
    # ---------------------------
    
    if search:
        all_products = [p for p in all_products if search in p.get('title', '').lower() or 
                        (p.get('identification') and p['identification'].get('sku') and search in p['identification']['sku'].lower())]
    
    total = len(all_products)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_products = all_products[start:end]
    
    return jsonify({
        "products": paginated_products,
        "total": total,
        "pages": math.ceil(total / per_page) if total > 0 else 1
    })

@admin_product_bp.route('/proxy-sync', methods=['POST'])
@login_required
def proxy_sync():
    return jsonify({"status": "success", "message": "تم تحديث البيانات من المصدر"})

@admin_product_bp.route('/save-sync', methods=['POST'])
@login_required
def save_sync():
    return jsonify({"status": "success", "message": "تم التخطي"})
