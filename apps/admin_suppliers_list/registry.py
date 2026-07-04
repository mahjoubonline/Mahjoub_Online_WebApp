# 📂 apps/admin_suppliers_list/registry.py

MODULE_NAME = "الموردون وشركاء النجاح"
MODULE_ICON = "fas fa-truck"  # أيقونة FontAwesome

# هنا نضع الروابط التي ستظهر في القائمة
LINKS = {
    "عرض الكل": "suppliers_bp.list_suppliers",
    "إضافة مورد جديد": "suppliers_bp.add_supplier"
}

def register_module(app):
    from apps.admin_suppliers_list.routes import suppliers_bp
    app.register_blueprint(suppliers_bp, url_prefix='/suppliers')
