# 📂 apps/admin_suppliers_list/registry.py

MODULE_NAME = "إدارة الموردين"
# استبدلت fa-users بـ bi-people-fill لتتوافق مع Bootstrap Icons وتحل مشكلة المربعات الفارغة
MODULE_ICON = "bi-people-fill" 

LINKS = {
    "قائمة الشركاء": "suppliers_bp.list_suppliers",
    "تعميد شريك جديد": "admin_suppliers_add_bp.add_supplier_or_staff"
}

def register_module(app):
    # تسجيل الروابط لكلا الموديولين هنا
    try:
        from .routes import suppliers_bp
        from apps.admin_suppliers_add.routes import admin_suppliers_add_bp
        
        app.register_blueprint(suppliers_bp, url_prefix='/admin/suppliers')
        app.register_blueprint(admin_suppliers_add_bp, url_prefix='/admin/suppliers_add')
        
        print("✅ [Registry]: تم تسجيل موديول 'suppliers' و 'suppliers_add' بنجاح تحت قسم إدارة الموردين.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديولات الموردين: {e}")
