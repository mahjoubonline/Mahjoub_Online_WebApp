# 📂 apps/admin_permissions/registry.py
from apps.admin_permissions.routes import admin_permissions_bp

MODULE_NAME = "إدارة الصلاحيات"
MODULE_ICON = "fas fa-user-shield"

# التصحيح: المسار البرمجي هو المفتاح (Key)، والاسم العربي هو القيمة (Value)
LINKS = {
    "admin_permissions.roles_list": "قائمة الصلاحيات"
}

def register_module(app):
    # هنا يتم تسجيل الـ Blueprint ديناميكياً
    app.register_blueprint(admin_permissions_bp, url_prefix='/admin/permissions')
    print("✅ [Registry]: تم تسجيل موديول 'إدارة الصلاحيات' بنجاح.")
