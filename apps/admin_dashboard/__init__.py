# coding: utf-8
# 🛡️ مستند تعريف النواة السيادية للوحة التحكم - منصة محجوب أونلاين 2026

from flask import Blueprint

# تعريف الـ Blueprint مع توحيد الاسم البرمجي لمنع انهيار الـ Workers أثناء الإقلاع
admin_dashboard_bp = Blueprint(
    'admin_dashboard', 
    __name__, 
    template_folder='templates'
)

# 🔄 استيراد المسارات أسفل التعريف ضروري جداً لربط الدوال ومنع التداخل الدائري (Circular Import)
from . import routes
