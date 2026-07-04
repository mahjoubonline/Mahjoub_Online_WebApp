# coding: utf-8
# 📂 apps/admin_suppliers_list/registry.py

# استيراد الـ Blueprint الصحيح من ملف routes
from .routes import suppliers_bp

# إعدادات العرض في الشريط الجانبي
MODULE_NAME = "إدارة الموردين"
MODULE_ICON = "fa-users"

# الربط الصحيح باستخدام اسم الـ Blueprint (suppliers_bp)
LINKS = {
    "قائمة الموردين": "suppliers_bp.list_suppliers",
    "إضافة مورد": "suppliers_bp.add_supplier"
}

def register_module(app):
    """تسجيل الـ Blueprint في التطبيق"""
    app.register_blueprint(suppliers_bp, url_prefix='/suppliers')
