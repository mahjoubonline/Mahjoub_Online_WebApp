# 📂 apps/admin_suppliers_add/registry.py
from .routes import admin_suppliers_add_bp

# الإعدادات للظهور في القائمة الجانبية
MODULE_NAME = "الموردين"
MODULE_ICON = "fas fa-user-plus"
LINKS = {
    "admin_suppliers_add_bp.index": "إضافة مورد جديد"
}

def register_module(app):
    try:
        app.register_blueprint(admin_suppliers_add_bp, url_prefix='/admin/suppliers_add')
        print("✅ [Registry]: تم تسجيل موديول 'admin_suppliers_add' بنجاح.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول التعميد: {e}")
