# 📂 apps/utils/translator.py

def translate_to_arabic(text):
    """
    تعريب أو معالجة نصوص وعناوين المنتجات القادمة حياً من قمرة.
    """
    if not text:
        return ""
    return text

def translate_status(status_key):
    """
    ترجمة الحالات التقنية للطلبات والمنتجات القادمة حياً من قمرة 
    إلى لغة عربية مفهومة في لوحة التحكم المركزية.
    """
    if not status_key:
        return "غير محدد"
        
    translations = {
        # حالات المنتجات الحية
        'active': 'مُفعل',
        'archived': 'مؤرشف',
        'draft': 'مسودة',
        'retired': 'متوقف',
        
        # حالات الطلبات الحية
        'pending': 'قيد الانتظار',
        'confirmed': 'مؤكد',
        'processing': 'تحت التنفيذ',
        'shipped': 'تم الشحن',
        'delivered': 'تم التسليم',
        'cancelled': 'ملغي'
    }
    
    return translations.get(status_key.lower().strip(), status_key)
