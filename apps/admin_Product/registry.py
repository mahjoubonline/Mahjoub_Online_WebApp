# coding: utf-8
# 📂 apps/admin_Product/registry.py

import apps.admin_Product.routes as product_routes

MODULE_NAME = "إدارة المنتجات"
MODULE_ICON = "fa-boxes"
SHOW_IN_SUPPLIER = False

LINKS = {
    "إدارة المنتجات": "/admin/products/",
    "إضافة منتج": "/admin/products/add",
    "مزامنة المنتجات": "/admin/products/sync"
}

def register_module(app):
    # تسجيل الـ Blueprint من الموديول مباشرة لتفادي الاستيراد الدائري
    app.register_blueprint(product_routes.admin_product_bp)
