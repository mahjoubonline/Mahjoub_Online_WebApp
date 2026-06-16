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
    ترجمة الحالات التقنية للطلبات والمنتجات والعمليات إلى لغة عربية مفهومة.
    """
    if not status_key:
        return "غير محدد"
        
    translations = {
        # حالات المنتجات
        'active': 'مُفعل',
        'archived': 'مؤرشف',
        'draft': 'مسودة',
        'retired': 'متوقف',
        
        # حالات الطلبات والعمليات المالية
        'pending': 'قيد الانتظار',
        'confirmed': 'مؤكد',
        'processing': 'تحت التنفيذ',
        'shipped': 'تم الشحن',
        'delivered': 'تم التسليم',
        'cancelled': 'ملغي',
        'paid': 'مدفوع',
        'unpaid': 'غير مدفوع'
    }
    
    return translations.get(status_key.lower().strip(), status_key)
