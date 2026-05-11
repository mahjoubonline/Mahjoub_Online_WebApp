# admin_panel/__init__.py
from flask import Blueprint
import logging

# 1. إعلان الهوية السيادية لمنطقة الإدارة (The Admin Core)
# الرابط الأساسي سيكون دائماً يبدأ بـ /admin
admin_bp = Blueprint(
    'admin', 
    __name__, 
    template_folder='templates', 
    static_folder='static', 
    url_prefix='/admin' 
)

# 2. بروتوكول الربط السيادي المحدث (Clean Sovereign Linkage)
# نستخدم هذا الترتيب لضمان استدعاء كافة المسارات تحت لواء الـ Blueprint
try:
    # أ- محرك الحماية والولوج (Login/Logout)
    from . import auth 
    
    # ب- محرك الرادار والداشبورد (Main Routes)
    from . import routes 
    
    # ج- محرك الخدمات السيادية (Suppliers Management & AJAX)
    # هذا هو الجسر الذي فعلناه لإدارة الموردين والحفظ التلقائي
    from . import supplier_service_routes 

    logging.info("✅ تم تعميد كافة محركات لوحة التحكم بنجاح.")

except ImportError as e:
    # بروتوكول تسجيل الأخطاء: يظهر في سجلات Railway لمساعدتك في التتبع
    logging.error(f"⚠️ تنبيه سيادي: تعذر استدعاء بعض الوحدات في لوحة التحكم: {e}")

"""
--- سجل التنقية والاستقرار (القائد علي محجوب) ---
1. تم توحيد إدارة الموردين تحت 'supplier_service_routes' لإنهاء التشتت.
2. تم ضبط url_prefix ليكون '/admin' لضمان تنظيم الروابط السيادية.
3. النظام الآن يتبع معايير Clean Architecture وجاهز للتشغيل الكامل.
"""
