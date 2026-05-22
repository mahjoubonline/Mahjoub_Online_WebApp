# coding: utf-8
# ⚙️ ملف تهيئة وحدة إدارة الموردين - منصة محجوب أونلاين 2026

from flask import Blueprint

# تعريف الـ Blueprint لمرة واحدة فقط مركزيّاً
admin_suppliers_bp = Blueprint(
    'add_supplier', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

# استيراد المسارات بعد تعريف الـ Blueprint لتجنب التداخل الدائري
from . import routes
