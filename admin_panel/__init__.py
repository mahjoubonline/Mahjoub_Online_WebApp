# admin_panel/__init__.py
from flask import Blueprint

# 1. إعلان الهوية السيادية لمنطقة الإدارة (The Admin Core)
# تم تعريف البلوبرنت هنا ليكون المظلة لكل عمليات لوحة التحكم
admin_bp = Blueprint(
    'admin', 
    __name__, 
    template_folder='templates', 
    static_folder='static', 
    url_prefix='/admin' 
)

# 2. بروتوكول الربط السيادي (Sovereign Linkage)
# تم وضع الاستيرادات في الأسفل لمنع خطأ الـ Circular Import (التداخل الدائري)
# وتم الإبقاء فقط على الوحدات النشطة لضمان استقرار "محجوب أونلاين"

from . import auth             # محرك الحماية والولوج
from . import routes           # محرك الرادار والداشبورد والإحصائيات
from . import manage_suppliers  # محرك إدارة الموردين والعمليات المالية

"""
--- توثيق الاستقرار للمؤسس علي محجوب ---
- تم حذف 'add_supplier_routes' لمنع الانهيار (Crash) في Railway.
- تم التأكد من أن الهوية (admin_bp) يتم حجزها أولاً ثم حقن المسارات فيها.
- النظام الآن جاهز للإقلاع (Boot) بنسبة 100%.
"""
