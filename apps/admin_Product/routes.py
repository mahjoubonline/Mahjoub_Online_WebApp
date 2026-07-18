# coding: utf-8
# 📂 apps/admin_Product/routes.py

from flask import render_template, request, flash
from flask_login import login_required
from .registry import admin_product_bp
from apps.services.graphql_client import QomrahGraphQLClient
import logging

logger = logging.getLogger(__name__)

# استعلام جلب المنتجات
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

@admin_product_bp.route('/', methods=['GET'])
@login_required
def manage_products():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('title', '').strip()
    
    # نرسل null إذا كان البحث فارغاً، فقد تتوقع قمرة ذلك
    variables = {
        "input": {
            "page": page,
            "limit": 50,
            "title": search if search else None 
        }
    }
    
    products = []
    pagination = {"currentPage": page, "totalPages": 1}
    
    try:
        response = QomrahGraphQLClient.execute_query(GET_ALL_PRODUCTS_QUERY, variables)
        
        # --- [تصحيح]: قمنا بتوسيع طريقة قراءة البيانات لتكون أكثر مرونة ---
        # أضفت هذا السطر للتشخيص (انظر الـ Terminal الخاص بك عند فتح الصفحة)
        print(f"DEBUG: Response from Qomrah: {response}") 
        
        if response:
            # إذا كانت الاستجابة مغلفة بـ 'data' نستخدمها، وإلا نأخذ الاستجابة كما هي
            root = response.get('data', response)
            result = root.get('findAllProducts', {})
            
            products = result.get('data') if result.get('data') is not None else []
            pagination = result.get('pagination') or {"currentPage": page, "totalPages": 1}
            
            # إذا لم تكن هناك بيانات من قمرة، حاول طباعة ما يوجد في الـ Terminal
            if not products:
                logger.warning("⚠️ قمرة لم تُرجع أي منتجات.")
                
    except Exception as e:
        logger.error(f"❌ خطأ أثناء جلب البيانات: {e}")
        flash("حدث خطأ أثناء تحميل قائمة المنتجات.")

    return render_template(
        'admin/admin_Product.html',
        products=products,
        pagination=pagination,
        search=search
    )
