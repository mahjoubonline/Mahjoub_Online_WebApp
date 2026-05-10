# admin_panel/__init__.py
from flask import Blueprint

# 1. إعلان الهوية السيادية لمنطقة الإدارة (The Admin Core)
# تم تعريف الكائن أولاً لضمان توفره للملفات الأخرى عند استدعائها
admin_bp = Blueprint(
    'admin', 
    __name__, 
    template_folder='templates', 
    static_folder='static', 
    url_prefix='/admin' 
)

# 2. بروتوكول الربط السيادي (Sovereign Linkage)
# ملاحظة تقنية للقائد علي: تم نقل الاستيرادات للأسفل لمنع خطأ الـ Circular Import
# لضمان استقرار النظام على سيرفرات Railway

from . import auth                 # محرك الحماية والولوج
from . import routes               # محرك الرادار والإحصائيات
from . import add_supplier_routes   # محرك التعميد السيادي الجديد
from . import manage_suppliers  # إضافة وحدة الإدارة الجديدة

"""
--- توثيق الهيكل السيادي للمؤسس علي محجوب (نسخة الاستقرار v3.5.1) ---
بهذا الترتيب المحدث، تم حل مشكلة التداخل البرمجي:
1. يتم حجز الهوية السيادية (admin_bp) في الذاكرة أولاً.
2. يتم حقن المسارات والمحركات (auth, routes, add_supplier_routes) داخل الهوية.

هذا الهيكل يضمن عدم توقف "محجوب أونلاين" عن العمل أثناء التحديثات البرمجية.
"""
