# coding: utf-8
# 📂 apps/admin_Product/registry.py

from .routes import admin_product_bp

MODULE_NAME = "إدارة المنتجات"
MODULE_ICON = "fa-boxes"
SHOW_IN_SUPPLIER = False

LINKS = {
    "إدارة المنتجات": "/admin/products/",
    "إضافة منتج": "/admin/products/add",
    "مزامنة المنتجات": "/admin/products/sync"
}

def register_module(app):
    app.register_blueprint(admin_product_bp)
