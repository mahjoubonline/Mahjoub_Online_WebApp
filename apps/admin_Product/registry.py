from flask import Blueprint
from .routes import admin_product_bp
# استيراد الملفات هنا لضمان تشغيل الكود بداخلها وبالتالي تسجيل الراوترات
from . import routes, routes_add, routes_edit, routes_sync

MODULE_NAME = "إدارة المنتجات"
MODULE_ICON = "fas fa-box-open"
SHOW_IN_SUPPLIER = False 

LINKS = {
    "admin_product_bp.manage_products": "قائمة المنتجات",
    "admin_product_bp.add_product": "إضافة منتج"
}

def register_module(app):
    try:
        app.register_blueprint(admin_product_bp, url_prefix='/admin/products')
        print("✅ [Registry]: تم تسجيل موديول 'إدارة المنتجات' بنجاح.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول 'إدارة المنتجات': {e}")
