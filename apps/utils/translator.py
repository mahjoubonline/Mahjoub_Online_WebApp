# 📂 apps/utils/translator.py
from deep_translator import GoogleTranslator

# ذاكرة مؤقتة لتخزين الترجمات السابقة وتسريع عرض الصفحات
_cache = {}

def translate_to_arabic(text):
    """
    دالة ترجمة فورية للنصوص مع نظام Caching للسرعة.
    تحول النصوص من الإنجليزية إلى العربية.
    """
    if not text:
        return ""
    
    # التحقق مما إذا كان النص قد تُرجم سابقاً لتجنب الاتصال المتكرر بـ API
    if text in _cache:
        return _cache[text]
    
    try:
        # القيام بعملية الترجمة
        translated = GoogleTranslator(source='en', target='ar').translate(text)
        
        # حفظ النتيجة في الذاكرة للطلبات القادمة
        _cache[text] = translated
        return translated
    except Exception as e:
        # في حال حدوث خطأ (مثل انقطاع الاتصال)، نعيد النص الأصلي لتجنب انهيار الصفحة
        print(f"⚠️ Translation Error: {e}")
        return text
