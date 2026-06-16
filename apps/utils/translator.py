# 📂 apps/utils/translator.py

def translate_status(status_key):
    """
    ترجمة الحالات البرمجية الخاصة بالطلبات والدفع والمصادر إلى اللغة العربية.
    """
    if not status_key:
        return "غير محدد"
        
    translations = {
        # حالات الطلب العامة (Order Status)
        'pending': 'قيد الانتظار',
        'confirmed': 'مؤكد',
        'processing': 'تحت التنفيذ',
        'shipped': 'تم الشحن',
        'delivered': 'تم التسليم',
        'cancelled': 'ملغي',
        'refunded': 'مسترد',
        'failed': 'فشل الدفع',
        
        # حالات الدفع المالية (Financial Status)
        'paid': 'مدفوع',
        'unpaid': 'غير مدفوع',
        
        # قنوات ومصادر الطلبات (Channels)
        'store': 'المتجر',
        'funnel': 'فانل تسويقي'
    }
    
    return translations.get(status_key.lower().strip(), status_key)
