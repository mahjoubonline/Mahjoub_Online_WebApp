# 📂 apps/admin_suppliers_add/registry.py
from .routes import admin_suppliers_add_bp

# الإعدادات للظهور في القائمة الجانبية
MODULE_NAME = "الموردين"
MODULE_ICON = "fas fa-user-plus"

# الربط البرمجي: Key يربط اسم الـ Blueprint باسم الدالة المحددة في routes.py
LINKS = {
    "admin_suppliers_add_bp.add_supplier_or_staff": "إضافة مورد جديد"
}

def register_module(app):
    try:
        # تسجيل الـ Blueprint بمسار مخصص لضمان تفرده
        app.register_blueprint(admin_suppliers_add_bp, url_prefix='/admin/suppliers_add')
        print("✅ [Registry]: تم تسجيل موديول 'admin_suppliers_add' بنجاح.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول التعميد: {e}")
