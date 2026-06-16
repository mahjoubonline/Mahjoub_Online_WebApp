# 📂 apps/utils/translator.py
from deep_translator import GoogleTranslator

_cache = {}

# قاموس مخصص للمصطلحات لضمان دقة العرض
_mapping = {
    # الأعمدة
    "_id": "رقم الطلب",
    "customer": "العميل",
    "createdAt": "تاريخ الإنشاء",
    "status": "حالة الطلب",
    "financialStatus": "حالة الدفع",
    "fulfillmentStatus": "حالة التجهيز",
    "paymentMethod": "وسيلة الدفع",
    "totalPrice": "المبلغ",
    "items": "المنتجات",
    
    # حالات الطلب
    "pending": "قيد الانتظار",
    "paid": "مدفوع",
    "processing": "تحت التنفيذ",
    "shipped": "تم الشحن",
    "delivered": "تم التسليم",
    "cancelled": "ملغي",
    "refunded": "مسترد",
    "failed": "فشل الدفع",
    
    # وسائل الدفع
    "cash_on_delivery": "دفع عند الاستلام",
    "bank_transfer": "تحويل بنكي",
    "credit_card": "بطاقة ائتمان",
    "wallet": "محفظة إلكترونية"
}

def translate(text):
    """ترجمة ديناميكية تعتمد على القاموس أولاً ثم الترجمة الذكية"""
    if text in _mapping:
        return _mapping[text]
    
    # تحويل القيم البرمجية (مثل camelCase) إلى نصوص مقروءة قبل الترجمة
    readable_text = "".join([c if c.islower() else f" {c}" for c in str(text)]).strip()
    
    if readable_text not in _cache:
        try:
            _cache[readable_text] = GoogleTranslator(source='en', target='ar').translate(readable_text)
        except:
            _cache[readable_text] = text
            
    return _cache[readable_text]
