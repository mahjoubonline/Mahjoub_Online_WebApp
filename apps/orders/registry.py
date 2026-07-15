# 📂 apps/admin_Product/registry.py
from .routes import admin_product_bp

MODULE_NAME = "إدارة المنتجات"
MODULE_ICON = "fas fa-box-open"

LINKS = {
    "قائمة المنتجات": "admin_product.manage_products",
    "إضافة منتج": "admin_product.add_product"
}

def register_module(app):
    try:
        app.register_blueprint(admin_product_bp, url_prefix='/admin/products')
        print(f"✅ [Registry]: تم تسجيل موديول 'Products' بنجاح تحت المسار /admin/products.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول 'Products': {e}")
