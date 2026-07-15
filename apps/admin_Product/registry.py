# 📂 apps/admin_Product/registry.py

# نستخدم الاستيراد النسبي للوصول إلى البلوبرينت المعرف في routes.py
from .routes import admin_product_bp

# إعدادات العرض في النظام الديناميكي
MODULE_NAME = "إدارة المنتجات"
MODULE_ICON = "fas fa-box-open"
LINKS = {
    "قائمة المنتجات": "admin_product.manage_products"
}

def register_module(app):
    """
    تسجيل موديول المنتجات الخاص بالمسؤول.
    """
    # التأكد من وجود البلوبرينت قبل تسجيله
    if admin_product_bp:
        # تسجيل البلوبرينت تحت المسار /admin/products
        app.register_blueprint(admin_product_bp, url_prefix='/admin/products')
        print(f"✅ [Registry]: تم تسجيل موديول 'admin_Product' بنجاح على المسار (/admin/products).")
    else:
        print(f"❌ [Registry]: فشل تسجيل 'admin_Product' - البلوبرينت غير معرف.")
