# coding: utf-8
# 📂 apps/admin_suppliers_add/registry.py

from apps.admin_suppliers_add.routes import admin_suppliers_add_bp

# تم إبقاء الاسم هنا، ولكن بما أن LINKS فارغ، لن يظهر هذا كقائمة جانبية منفصلة
MODULE_NAME = "إضافة مورد" 
MODULE_ICON = "fa-user-plus"

# ✅ الحل: تفريغ القائمة ليتم تجاهل هذا الموديول في القائمة الجانبية
LINKS = {} 

def register_module(app):
    """
    تسجيل موديول الإضافة برمجياً فقط
    """
    try:
        app.register_blueprint(admin_suppliers_add_bp, url_prefix='/admin/suppliers')
        print("✅ [Registry]: تم تسجيل موديول 'admin_suppliers_add' بنجاح (مخفي من القائمة).")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول 'admin_suppliers_add': {e}")
