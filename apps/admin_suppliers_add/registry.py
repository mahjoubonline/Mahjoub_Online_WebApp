# coding: utf-8
from .routes import suppliers_bp

MODULE_NAME = "إدارة الشركاء"
MODULE_ICON = "fa-users"

# هنا نجمع كل الروابط الخاصة بالموردين
LINKS = {
    "قائمة الشركاء": "suppliers_bp.list_suppliers",
    "تعميد شريك": "admin_suppliers_add_bp.add_supplier_or_staff"
}

def register_module(app):
    try:
        app.register_blueprint(suppliers_bp, url_prefix='/admin/suppliers')
        print("✅ [Registry]: تم تسجيل موديول 'admin_suppliers_list' بنجاح.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول 'admin_suppliers_list': {e}")
