# 📂 apps/utils/products_engine.py

# استخدام المسارات المطلقة (Absolute Imports) لمنع فشل الـ Build
from apps.utils.bridge_engine import execute_query
from apps.utils.translator import translate_to_arabic

def get_products_by_supplier(supplier_tag):
    """
    جلب منتجات المورد من المحرك، مع معالجة العناوين للغة العربية.
    """
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
    
    # تنفيذ الاستعلام عبر محرك الجسر السيادي
    result = execute_query(query, variables)
    
    # التحقق من وجود بيانات
    if not result or 'data' not in result:
        return []
        
    products = result.get('data', {}).get('products', [])
    
    # معالجة البيانات: ترجمة العناوين للعربية
    for p in products:
        if 'title' in p and p['title']:
            p['title'] = translate_to_arabic(p['title'])
            
    return products

def get_product_status_translation(status):
    """
    مترجم للحالات البرمجية للمنتجات.
    """
    translations = {
        'active': 'مُفعل',
        'archived': 'مؤرشف',
        'draft': 'مسودة',
        'retired': 'متوقف'
    }
    return translations.get(status.lower(), status)
