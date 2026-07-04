# coding: utf-8
# 📂 apps/admin_suppliers_add/registry.py

from .routes import admin_suppliers_add_bp # تأكد من اسم الـ Blueprint لديك

MODULE_NAME = "إدارة الموردين"
MODULE_ICON = "fa-user-plus"

# تم تسطيح الروابط هنا أيضاً
LINKS = {
    "تعميد شريك": "admin_suppliers_add_bp.add_supplier_or_staff"
}

def register_module(app):
    try:
        app.register_blueprint(admin_suppliers_add_bp, url_prefix='/admin/suppliers_add')
        print("✅ [Registry]: تم تسجيل موديول 'admin_suppliers_add' بنجاح.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول 'admin_suppliers_add': {e}")
