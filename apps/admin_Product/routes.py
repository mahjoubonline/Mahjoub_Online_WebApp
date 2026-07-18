# coding: utf-8
# 📂 apps/admin_Product/routes.py

from flask import render_template, request, flash
from flask_login import login_required
from .registry import admin_product_bp  # تم تعديل الاستيراد ليتطابق تماماً مع موديول المزامنة
from apps.services.graphql_client import QomrahGraphQLClient

# استعلام جلب المنتجات من واجهة قمرة
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
    
    # جلب 100 منتج لضمان وجود كمية كافية لتصفيتها محلياً بواسطة بايثون
    variables = {
        "input": {
            "page": page,
            "limit": 100,
            "title": search if search else None
        }
    }
    
    products = []
    pagination = {"currentPage": page, "totalPages": 1}
    
    try:
        response = QomrahGraphQLClient.execute_query(GET_ALL_PRODUCTS_QUERY, variables)
        
        if response and 'findAllProducts' in response:
            result = response['findAllProducts']
            all_products = result.get('data', []) or []
            
            # تفعيل عملية الفلترة النصية (CONTAINS) محلياً داخل السيرفر
            if search:
                products = [
                    p for p in all_products 
                    if p.get('title') and search.lower() in str(p.get('title')).lower()
                ]
                # تثبيت الترقيم لصفحة واحدة عند ظهور نتائج الفلترة المخصصة
                pagination = {"currentPage": 1, "totalPages": 1}
            else:
                products = all_products
                pagination = result.get('pagination', {"currentPage": page, "totalPages": 1})
                
    except Exception as e:
        print(f"❌ خطأ في موديول المنتجات أثناء الفلترة: {e}")
        flash("حدث خطأ أثناء معالجة البيانات.")

    return render_template(
        'admin/admin_product.html',
        products=products,
        pagination=pagination,
        search=search
    )
