from flask import Blueprint

# 1. تعريف البلوبرنت (Blueprint) للإدارة
# تم تحديد template_folder لضمان قراءة القوالب من المجلد الفرعي المنظم
admin_bp = Blueprint(
    'admin_panel', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

# 2. استيراد المسارات (Routes)
# يجب الاستيراد في الأسفل لتجنب خطأ الاستيراد الدائري (Circular Import)
try:
    from . import routes
    print("🏰 [System] تم تجهيز بوابة الإدارة السيادية.")
except ImportError as e:
    print(f"⚠️ [Error] فشل في تحميل مسارات الإدارة: {e}")

# تصدير الكائن ليكون متاحاً للنواة
__all__ = ['admin_bp']
