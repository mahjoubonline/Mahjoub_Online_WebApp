from flask import Blueprint

# 1. تعريف البلوبرنت (Blueprint)
# تم تحديد مجلد القوالب الافتراضي 'templates'
supplier_bp = Blueprint(
    'supplier_panel', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

# 2. ربط المكونات (🚨 السطر الأهم لحل مشكلة 404)
# نقوم باستيراد الملفات هنا لضمان تسجيل الروابط والحماية عند تشغيل التطبيق
try:
    from . import routes 
    from . import auth_logic
    from . import decorators
    
    print("🚀 [System] تم تفعيل بوابة الموردين السيادية بنجاح.")
    
except ImportError as e:
    print(f"⚠️ [Critical Error] فشل في ربط مكونات بوابة الموردين: {e}")

# تصدير الكائن ليكون متاحاً للنواة المركزية
__all__ = ['supplier_bp']
