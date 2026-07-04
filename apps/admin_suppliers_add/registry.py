# 📂 apps/admin_suppliers_add/registry.py

from apps.admin_suppliers_add.routes import admin_suppliers_add_bp

# إعدادات الموديول للظهور في القائمة الجانبية
MODULE_NAME = "إدارة الموردين"
MODULE_ICON = "fa-user-plus"

# تعريف الروابط المتاحة لهذا الموديول فقط
# تم حصر الرابط هنا لضمان عدم تكرار ظهور "إدارة الموردين" في القائمة
LINKS = {
    "إضافة مورد جديد": "admin_suppliers_add_bp.add_supplier_or_staff"
}

def register_module(app):
    """
    دالة تسجيل الموديول في التطبيق الرئيسي
    """
    try:
        app.register_blueprint(admin_suppliers_add_bp, url_prefix='/admin/suppliers')
        print("✅ [Registry]: تم تسجيل موديول 'admin_suppliers_add' بنجاح.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول 'admin_suppliers_add': {e}")
