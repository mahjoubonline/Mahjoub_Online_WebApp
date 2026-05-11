# admin_panel/__init__.py
from flask import Blueprint

# 1. إعلان الهوية السيادية لمنطقة الإدارة (The Admin Core)
# هذا الكائن هو "المظلة" التي تجتمع تحتها كافة مسارات لوحة التحكم
admin_bp = Blueprint(
    'admin', 
    __name__, 
    template_folder='templates', 
    static_folder='static', 
    url_prefix='/admin' 
)

# 2. بروتوكول الربط السيادي المحدث (Clean Sovereign Linkage)
# تم تنظيف الاستدعاءات لضمان أعلى مستويات الاستقرار البرمجي
try:
    # أ- محرك الحماية والولوج: المسؤول عن تأمين الدخول والخروج
    from . import auth                     
    
    # ب- محرك الرادار والداشبورد: المسؤول عن الواجهة الرئيسية والإحصائيات
    from . import routes                   
    
    # ج- محرك الخدمات السيادية: المسؤول عن تعديل وحفظ بيانات الموردين
    # ملاحظة: تم استبدال الملفات القديمة بهذا المحرك المنظم
    from . import supplier_service_routes  

except ImportError as e:
    # بروتوكول تسجيل الأخطاء في سجلات Railway
    import logging
    logging.error(f"⚠️ تنبيه سيادي: تعذر استدعاء بعض الوحدات في لوحة التحكم: {e}")

"""
--- سجل التنظيف والتعميد النهائي (القائد علي محجوب) ---
1. تم حذف 'manage_suppliers' نهائياً لإنهاء مشكلة الـ Import المفقود.
2. تم توحيد مسارات الموردين تحت 'supplier_service_routes'.
3. النظام الآن يتبع معايير النقاء البرمجي (Clean Code) وجاهز للإقلاع.
"""
