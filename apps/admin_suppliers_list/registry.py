# 📂 apps/admin_suppliers_add/registry.py
from .routes import admin_suppliers_add_bp

# تعيين الاسم لـ None يمنع ظهوره كموديول منفصل في القائمة الجانبية
MODULE_NAME = None 

def register_module(app):
    try:
        app.register_blueprint(admin_suppliers_add_bp, url_prefix='/admin/suppliers_add')
        print("✅ [Registry]: تم تسجيل إضافة الموردين برمجياً.")
    except Exception as e:
        print(f"❌ [Registry Error]: {e}")
