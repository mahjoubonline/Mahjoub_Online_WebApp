# admin_panel/__init__.py
from flask import Blueprint

# 1. تعريف الـ Blueprint أولاً كقاعدة أساسية لمنطقة الإدارة
# يتم تحديد مجلدات القوالب والملفات الثابتة لضمان استقرار العرض في محجوب أونلاين
admin_bp = Blueprint(
    'admin', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

# 2. استيراد المسارات والعمليات لربطها بالنظام
# وضع الاستيرادات هنا يكسر حلقة التداخل (Circular Import) ويضمن بدء تشغيل السيرفر بأمان
from . import routes
from . import auth

# ربط محرك إدارة الموردين (النافذة الأفقية) بالنظام لضمان عمل "السحب" و"التعديل"
from . import manage_suppliers
