# coding: utf-8
# 📂 apps/admin_suppliers_list/registry.py

from .routes import suppliers_bp
# استيراد الـ Blueprint الخاص بالموديول الآخر من مساره
from apps.admin_suppliers_add.routes import admin_suppliers_add_bp 

MODULE_NAME = "إدارة الموردين"
MODULE_ICON = "fa-users"

LINKS = {
    "قائمة الشركاء": "suppliers_bp.list_suppliers",
    "تعميد شريك": "admin_suppliers_add_bp.add_supplier_or_staff"
}

def register_module(app):
    try:
        # تسجيل الموديول الأول
        app.register_blueprint(suppliers_bp, url_prefix='/admin/suppliers')
        # تسجيل الموديول الثاني من هنا
        app.register_blueprint(admin_suppliers_add_bp, url_prefix='/admin/suppliers_add')
        
        print("✅ [Registry]: تم تسجيل موديولات الموردين بنجاح.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل التسجيل: {e}")
