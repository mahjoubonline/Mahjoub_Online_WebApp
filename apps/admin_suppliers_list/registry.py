# coding: utf-8
# 📂 apps/admin_suppliers_list/registry.py

# استيراد الـ Blueprint من ملف routes الخاص بهذا الموديول
from .routes import admin_suppliers_list_bp

# 1. إعدادات ظهور الموديول في الشريط الجانبي
MODULE_NAME = "إدارة الموردين"  # الاسم الذي سيظهر في القائمة
MODULE_ICON = "fa-users"        # الأيقونة (من FontAwesome)
LINKS = {
    "قائمة الموردين": "admin_suppliers_list_bp.suppliers_list",
    "سجل الموردين": "admin_suppliers_list_bp.suppliers_logs"
}

# 2. دالة التسجيل التي يستدعيها الـ Auto-Discovery
def register_module(app):
    """
    تسجيل الـ Blueprint الخاص بهذا الموديول في تطبيق Flask
    """
    app.register_blueprint(admin_suppliers_list_bp, url_prefix='/suppliers')
