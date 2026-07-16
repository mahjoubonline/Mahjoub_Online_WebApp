# 📂 apps/admin_permissions/registry.py
from .routes import admin_permissions_bp

MODULE_NAME = "إدارة الصلاحيات"
MODULE_ICON = "fas fa-shield-alt"

LINKS = {
    "admin_permissions_bp.roles_list": "قائمة الموظفين والصلاحيات"
}

def register_module(app):
    try:
        app.register_blueprint(admin_permissions_bp, url_prefix='/admin/permissions')
        print("✅ [Registry]: تم تسجيل موديول الصلاحيات بنجاح.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول الصلاحيات: {e}")
