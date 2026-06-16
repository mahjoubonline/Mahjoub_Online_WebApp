# 📂 apps/utils/translator.py
from deep_translator import GoogleTranslator

_cache = {}

# قاموس مخصص للمصطلحات لضمان دقة العرض
_mapping = {
    # الحقول
    "_id": "رقم الطلب",
    "customer": "العميل",
    "createdAt": "تاريخ الإنشاء",
    "status": "حالة الطلب",
    "financialStatus": "حالة الدفع",
    "fulfillmentStatus": "حالة التجهيز",
    "totalPrice": "المبلغ",
    "items": "المنتجات",
    # الحالات
    "pending": "قيد الانتظار",
    "paid": "مدفوع",
    "processing": "تحت التنفيذ",
    "shipped": "تم الشحن",
    "delivered": "تم التسليم",
    "cancelled": "ملغي",
    "refunded": "مسترد",
    "failed": "فشل الدفع"
}

def translate(text):
    """ترجمة ديناميكية مع الاعتماد على القاموس أولاً"""
    if text in _mapping:
        return _mapping[text]
    
    if text not in _cache:
        try:
            _cache[text] = GoogleTranslator(source='en', target='ar').translate(text)
        except:
            _cache[text] = text
    return _cache[text]
