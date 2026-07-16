# 📂 apps/admin_suppliers_list/registry.py

# نقوم باستيراد البلوبرينتات من ملفاتها الصحيحة
from .routes import suppliers_bp
from apps.admin_suppliers_add.routes import admin_suppliers_add_bp

MODULE_NAME = "إدارة الموردين"
MODULE_ICON = "fas fa-users"

LINKS = {
    "suppliers_bp.list_suppliers": "قائمة الشركاء",
    "admin_suppliers_add_bp.add_supplier_or_staff": "تعميد شريك جديد"
}

def register_module(app):
    try:
        # تسجيل كلاهما هنا
        app.register_blueprint(suppliers_bp, url_prefix='/admin/suppliers')
        app.register_blueprint(admin_suppliers_add_bp, url_prefix='/admin/suppliers_add')
        print("✅ [Registry]: تم تسجيل موديول 'الموردين' بالكامل.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل الموديول: {e}")
