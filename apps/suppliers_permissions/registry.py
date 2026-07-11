# 📂 apps/suppliers_permissions/registry.py

from apps.suppliers_permissions.routes import suppliers_permissions_bp

MODULE_NAME = "إدارة الصلاحيات"
MODULE_ICON = "fas fa-users-cog"

# هذا السطر هو مفتاح ظهور الرابط في الشريط الجانبي
LINKS = {
    "suppliers_permissions.permissions": "صلاحيات الموظفين"
}

SHOW_IN_SUPPLIER = True

def register_module(app):
    app.register_blueprint(suppliers_permissions_bp, url_prefix='/supplier')
