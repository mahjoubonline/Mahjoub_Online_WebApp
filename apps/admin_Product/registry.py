# coding: utf-8
# 📂 apps/admin_Product/registry.py

import apps.admin_Product.routes as product_routes

# بيانات الموديول للظهور في الشريط الجانبي
MODULE_NAME = "إدارة المنتجات"
MODULE_ICON = "fa-boxes"
SHOW_IN_SUPPLIER = False

# الروابط التي ستظهر في القائمة الجانبية
LINKS = {
    "المنتجات": "/admin/products/",
    "إضافة منتج": "/admin/products/add"
}

def register_module(app):
    # تسجيل الـ Blueprint من ملف routes
    app.register_blueprint(product_routes.admin_product_bp)
