from flask import Blueprint

# 1. تعريف الـ Blueprint الخاص بلوحة الإدارة (مركز القيادة السيادي)
# نحدد مجلد القوالب 'templates' لضمان قراءة ملفات مثل dashboard.html و manage_suppliers.html
admin_bp = Blueprint(
    'admin', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

# 2. استيراد المسارات (Routes) في النهاية لتجنب مشكلة "التداخل الدائري" (Circular Import)
# هذا السطر هو الذي يربط الملف بالمسارات التي كتبناها (dashboard, manage-suppliers, الخ)
from . import routes
