# coding: utf-8
from flask import Blueprint, render_template, request
from flask_login import login_required
from apps.services.graphql_client import QomrahGraphQLClient
import logging

# تعريف الـ Blueprint
admin_product_bp = Blueprint('admin_product_bp', __name__, template_folder='templates')
logger = logging.getLogger(__name__)

# استيراد الوظائف الأخرى (تأكد أن الملفات الأخرى لا تعيد تعريف الـ Blueprint بنفس الاسم)
from . import routes_add, routes_edit, routes_sync

@admin_product_bp.route('/', methods=['GET'])
@login_required
def manage_products():
    # استقبال المتغيرات
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').strip()
    
    # إذا كان هناك بحث، نزيد الـ limit لجلب نتائج أكثر في الصفحة الواحدة
    limit = 100 if search else 20
    
    variables = {"input": {"page": page, "limit": limit}}
    if search:
        variables["input"]["search"] = search
    
    # الاستعلام
    query = """
    query Data($input: GetAllProductsInput) {
      findAllProducts(input: $input) {
        data { qid, title, quantity, pricing { price }, images { fileUrl } }
        pagination { totalPages, currentPage, totalItems }
      }
    }
    """
    
    try:
        result = QomrahGraphQLClient.execute_query(query, variables=variables) or {}
    except Exception as e:
        logger.error(f"GraphQL Error: {e}")
        result = {}

    data = result.get('findAllProducts', {})
    products = data.get('data', [])
    pag_info = data.get('pagination', {"totalPages": 1, "currentPage": 1, "totalItems": 0})
    
    return render_template('admin/admin_Product.html', 
                           products=products, 
                           pagination=pag_info, 
                           search=search)

# --- تسجيل الموديول (يُستخدم في ملف __init__.py الرئيسي) ---
MODULE_NAME = "إدارة المنتجات"
MODULE_ICON = "fas fa-box-open"
SHOW_IN_SUPPLIER = False 

LINKS = {
    "admin_product_bp.manage_products": "قائمة المنتجات",
    "admin_product_bp.add_product": "إضافة منتج"
}

def register_module(app):
    try:
        app.register_blueprint(admin_product_bp, url_prefix='/admin/products')
        print("✅ [Registry]: تم تسجيل موديول 'إدارة المنتجات' بنجاح.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول 'إدارة المنتجات': {e}")
