# 📂 apps/admin_suppliers_list/registry.py
from apps.admin_suppliers_list.routes import suppliers_bp

# أضف هذه المتغيرات لكي يراها نظام التسجيل التلقائي
MODULE_NAME = "سجل الشركاء"
MODULE_ICON = "fa-users"
LINKS = {
    "قائمة الشركاء": "suppliers_bp.list_suppliers" # تأكد من مطابقة اسم الـ endpoint في routes.py
}

def register_module(app):
    """تسجيل موديول 'سجل الشركاء'."""
    app.register_blueprint(suppliers_bp, url_prefix='/admin/suppliers')
    print("✅ [Registry]: تم تسجيل موديول 'admin_suppliers_list' بنجاح.")
