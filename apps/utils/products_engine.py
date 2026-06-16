# 📂 apps/utils/products_engine.py

# تم تصحيح المسار إلى المسار الكامل لتجنب خطأ ModuleNotFoundError
from apps.utils.bridge_engine import execute_query

def get_products_by_supplier(supplier_tag):
    """جلب المنتجات الخاصة بمورد محدد عبر الـ Tag"""
    query = """
    query GetProducts($query: String) {
      products(query: $query) {
        id
        title
        status
        tags
      }
    }
    """
    variables = {"query": f"tags:{supplier_tag}"}
    result = execute_query(query, variables)
    return result.get('data', {}).get('products', []) if result else []

def translate_product_status(status):
    """
    دالة المترجم السيادي: تحويل حالات المنتجات من الإنجليزية إلى العربية
    مثال: active -> مفعل، archived -> مؤرشف
    """
    translations = {
        'active': 'مُفعل',
        'archived': 'مؤرشف',
        'draft': 'مسودة',
        'retired': 'متوقف'
    }
    # يعيد القيمة المترجمة أو الحالة الأصلية إذا لم توجد ترجمة
    return translations.get(status.lower(), status)
