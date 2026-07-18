# coding: utf-8
# 📂 apps/admin_Product/registry.py

from flask import Blueprint, render_template, request
from flask_login import login_required
from apps.services.graphql_client import QomrahGraphQLClient
from apps.services.graphql_queries import GET_ALL_PRODUCTS
import logging

# [خطوة 1]: تعريف الـ Blueprint وتجهيز الـ Logger أولاً ليكون متاحاً في الذاكرة
admin_product_bp = Blueprint('admin_product_bp', __name__, template_folder='templates')
logger = logging.getLogger(__name__)

@admin_product_bp.route('/', methods=['GET'])
@login_required
def manage_products():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('title', request.args.get('search', '')).strip()
    
    limit = 100 if search else 20
    variables = {"input": {"page": page, "limit": limit}}
    if search:
        variables["input"]["title"] = search
    
    try:
        result = QomrahGraphQLClient.execute_query(GET_ALL_PRODUCTS, variables=variables) or {}
    except Exception as e:
        logger.error(f"❌ GraphQL Error inside registry: {e}")
        result = {}

    data = result.get('findAllProducts', {})
    all_products = data.get('data', []) or []
    pag_info = data.get('pagination', {"totalPages": 1, "currentPage": 1, "totalItems": 0})
    
    if search:
        products = [
            p for p in all_products 
            if p.get('title') and search.lower() in str(p.get('title')).lower()
        ]
        pag_info = {"totalPages": 1, "currentPage": 1, "totalItems": len(products)}
    else:
        products = all_products
    
    return render_template('admin/admin_Product.html', 
                           products=products, 
                           pagination=pag_info, 
                           search=search)

# --- إعدادات ربط وتسجيل الموديول مع النظام الرئيسي ---
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
        print("✅ [Registry]: تم تسجيل موديول 'إدارة المنتجات' بنجاح وتجاوز التعارض الدائري.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول 'إدارة المنتجات': {e}")

# [خطوة 2]: نقل استيراد المسارات الفرعية إلى نهاية الملف تماماً 🚀
# بهذه الطريقة عندما تفتح هذه الملفات وتستورد admin_product_bp ستجده معرّفاً وجاهزاً في الأعلى!
from . import routes_add, routes_edit, routes_sync
