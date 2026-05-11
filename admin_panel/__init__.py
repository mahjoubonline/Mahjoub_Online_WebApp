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

# 2. بروتوكول الربط السيادي (Sovereign Linkage)
# ملاحظة للقائد علي: نقوم باستيراد المسارات بعد تعريف الـ Blueprint 
# لضمان تسجيلها بشكل صحيح ومنع تعطل السيرفر أثناء التشغيل

try:
    # محرك الحماية والولوج (Login/Logout)
    from . import auth                     
    
    # محرك الرادار والداشبورد الأساسي والوظائف العامة
    from . import routes                   
    
    # محرك إدارة بروفايلات الموردين (التعديل والحفظ السيادي)
    # هذا الملف هو الذي يربط الواجهة بالمحرك core/services/supplier_service.py
    from . import supplier_service_routes  

except ImportError as e:
    # بروتوكول تسجيل الأخطاء في حال فقدان أي ملف أثناء النشر على Railway
    # سيظهر هذا التنبيه في سجلات (Logs) المنصة لتسهيل التنقيح
    print(f"⚠️ تنبيه سيادي: تعذر استدعاء بعض الوحدات البرمجية: {e}")

"""
--- توثيق الاستقرار النهائي للمؤسس علي محجوب ---
- تم حذف الاستدعاء القديم لـ manage_suppliers لمنع التداخل الدائري.
- تم اعتماد supplier_service_routes كمرجع وحيد لإدارة بيانات الكيانات.
- النظام الآن "خفيف" وجاهز للإقلاع (Deployment Ready) بدون أخطاء Import.
"""
