# coding: utf-8
# 📂 apps/admin_suppliers_add/registry.py

from .routes import admin_suppliers_add_bp 

# ملاحظة: تم حذف MODULE_NAME و LINKS من هنا متعمداً.
# لأننا قمنا بنقل تعريفات الروابط والاسم إلى ملف الموديول الرئيسي (admin_suppliers_list/registry.py).
# بهذا الشكل، سيعمل الموديول في الخلفية ولن يظهر كقائمة مكررة في الشريط الجانبي.

def register_module(app):
    try:
        app.register_blueprint(admin_suppliers_add_bp, url_prefix='/admin/suppliers_add')
        print("✅ [Registry]: تم تسجيل موديول 'admin_suppliers_add' بنجاح (بدون تكرار في القائمة).")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول 'admin_suppliers_add': {e}")
