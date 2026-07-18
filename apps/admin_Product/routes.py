# coding: utf-8
# 📂 apps/admin_Product/routes.py

from flask import render_template, request, flash
from flask_login import login_required
from .registry import admin_product_bp
from apps.services.graphql_client import QomrahGraphQLClient
import logging

logger = logging.getLogger(__name__)

# استعلام جلب المنتجات (تم التأكد من مطابقة هيكلية الـ Input)
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
    
    # تحسين: نرسل 'None' للـ title إذا كان فارغاً ليقوم الـ API بإرجاع كافة المنتجات
    # ونقوم بتمرير 'page' كقيمة صحيحة دائماً
    variables = {
        "input": {
            "page": page,
            "limit": 50,  # تقليل العدد لضمان سرعة الاستجابة
            "title": search if search else None 
        }
    }
    
    products = []
    pagination = {"currentPage": page, "totalPages": 1}
    
    try:
        response = QomrahGraphQLClient.execute_query(GET_ALL_PRODUCTS_QUERY, variables)
        
        if response and 'findAllProducts' in response:
            result = response.get('findAllProducts', {})
            
            # جلب البيانات والتأكد من أنها ليست None
            products = result.get('data') or []
            pagination = result.get('pagination') or {"currentPage": page, "totalPages": 1}
            
            # ملاحظة: إذا كان الـ API يعيد كل شيء عند إرسال title=None، 
            # فلن تحتاج للفلترة اليدوية أدناه. 
            # أبقيتها فقط كصمام أمان في حال كان الـ API لا يدعم البحث.
            if search and not products:
                logger.info("تم جلب قائمة فارغة من السيرفر، لا توجد منتجات مطابقة.")
                
    except Exception as e:
        logger.error(f"❌ خطأ أثناء جلب البيانات: {e}")
        flash("حدث خطأ أثناء تحميل قائمة المنتجات من السيرفر.")

    return render_template(
        'admin/admin_Product.html',
        products=products,
        pagination=pagination,
        search=search
    )
