# في ملف apps/admin_Product/routes_edit.py

from apps.models.product_db import Product # (فقط إذا أردت التحقق من السجلات المالية المرتبطة بالمنتج)
from apps.models.suppliers_db import Supplier

@admin_product_bp.route('/edit/<qid>', methods=['GET'])
@login_required
def edit_product(qid):
    try:
        # 1. جلب بيانات المنتج من قمرة (المصدر الوحيد للحقيقة)
        result = QomrahGraphQLClient.execute_query(FIND_PRODUCT_QUERY, variables={"qid": qid}) or {}
        product = result.get('findProductByQid')
        
        if not product:
            return "المنتج غير موجود في قمرة", 404
            
        # 2. البحث فقط عن المورد المرتبط بهذا الـ QID في قاعدة بياناتنا
        # بما أننا لا نحفظ بيانات المنتج، نبحث عن سجل ربط (إذا كان لديك جدول وسيط) 
        # أو نكتفي بجلب قائمة الموردين ليختار المشرف منها.
        suppliers = Supplier.query.all()
        
        # يمكنك جلب المورد الحالي المرتبط بهذا المنتج لو وجد
        # current_supplier = ... 
        
        return render_template(
            'admin/admin_edit_product.html', 
            product=product,
            suppliers=suppliers # نمرر القائمة للواجهة
        )
        
    except Exception as e:
        logger.error(f"Error fetching product {qid}: {e}")
        return "حدث خطأ أثناء جلب بيانات المنتج", 500
