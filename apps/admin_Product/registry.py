# apps/admin_Product/registry.py

MODULE_NAME = "admin_product"

# تعريف موديول إدارة المنتجات للقيادة المركزية
MODULE_CONFIG = {
    "display_name": "إدارة المنتجات",
    "icon": "fas fa-boxes",
    "links": {
        # المفتاح هو اسم الـ Endpoint كاملاً (اسم الـ Blueprint + اسم الدالة)
        # والقيمة هي النص الذي يظهر في القائمة المنسدلة
        "admin_product_bp.manage_products": "قائمة المنتجات",
        "admin_product_bp.add_product": "إضافة منتج",
    }
}

def register(registry_dict):
    """
    دالة تسجيل الموديول داخل قاموس الموديولات المسجلة (registered_modules)
    """
    registry_dict[MODULE_NAME] = MODULE_CONFIG
    return registry_dict
