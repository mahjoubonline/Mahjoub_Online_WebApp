from flask import Blueprint
import os

# 1. تعريف البلوبرنت (Blueprint) الخاص بلوحة الإدارة
# تم تحديد المسارات بدقة لضمان وصول المحرك للقوالب والملفات الساكنة
admin_bp = Blueprint(
    'admin_panel', 
    __name__, 
    template_folder='templates',  # المجلد الذي يحتوي على login.html و dashboard.html
    static_folder='static'        # المجلد الذي يحتوي على ملفات CSS/JS الخاصة بالإدارة
)

# 2. استيراد المسارات (Routes)
# يتم الاستيراد في أسفل الملف لكسر حلقة الاستيراد الدائري (Circular Import)
# لضمان أن كائن admin_bp قد تم تعريفه بالكامل قبل أن يطلبه ملف routes.py
try:
    from . import routes
    print("🏰 [System] تم تعميد بوابة الإدارة بنجاح.")
except Exception as e:
    # هذا التنبيه سيظهر في سجلات (Logs) Railway إذا كان هناك خلل في ملف routes.py
    print(f"⚠️ [Error] فشل في تحميل مسارات الإدارة: {str(e)}")

# تصدير الكائن ليكون متاحاً للاستدعاء من المحرك المركزي core/__init__.py
__all__ = ['admin_bp']
