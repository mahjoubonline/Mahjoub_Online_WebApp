# coding: utf-8
# 📂 apps/admin_suppliers_add/registry.py

from .routes import admin_suppliers_add_bp

# المتغيرات القياسية التي يكتشفها نظام الـ Auto-Discovery تلقائياً للحقن في الشريط الجانبي (الهيكل)
MODULE_NAME = "إدارة المتاجر والموردين"
MODULE_ICON = "fas fa-store shadow-sm"
LINKS = {
    "إضافة متجر / موظف": "admin_suppliers_add_bp.add_supplier_or_staff"
}

def register_module(app):
    """
    تسجيل موديول إدارة المتاجر والموردين (admin_suppliers_add) تلقائياً في مصنع التطبيق.
    """
    if admin_suppliers_add_bp:
        # تسجيل البلوبرينت بالمسار السيادي المعتمد
        app.register_blueprint(admin_suppliers_add_bp, url_prefix='/admin/suppliers')
        print("✅ [Registry]: تم تسجيل موديول 'admin_suppliers_add' بنجاح على المسار (/admin/suppliers).")
    else:
        print("❌ [Registry]: فشل تسجيل 'admin_suppliers_add' - البلوبرينت غير معرف في routes.py.")
