# coding: utf-8
from .routes import admin_suppliers_add_bp

# إزالة MODULE_NAME و LINKS من هنا يمنع ظهور موديول مكرر في الشريط الجانبي
# النظام سيستخدم اسم المجلد كبديل، ولكن طالما لا توجد روابط، لن تظهر قائمة فارغة.

def register_module(app):
    try:
        app.register_blueprint(admin_suppliers_add_bp, url_prefix='/admin/suppliers_add')
        print("✅ [Registry]: تم تسجيل موديول 'admin_suppliers_add' (بدون قائمة).")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل الموديول: {e}")
