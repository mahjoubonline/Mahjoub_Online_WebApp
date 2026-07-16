# 📂 apps/admin_suppliers_list/registry.py
from .routes import suppliers_bp

MODULE_NAME = "إدارة الموردين"
MODULE_ICON = "fas fa-users"

# هنا السر: نضع روابط الموديولين معاً في مكان واحد
LINKS = {
    "suppliers_bp.list_suppliers": "قائمة الشركاء",
    "admin_suppliers_add_bp.add_supplier_or_staff": "تعميد شريك جديد"
}

def register_module(app):
    try:
        app.register_blueprint(suppliers_bp, url_prefix='/admin/suppliers')
        print("✅ [Registry]: تم تسجيل موديول الموردين.")
    except Exception as e:
        print(f"❌ [Registry Error]: {e}")
