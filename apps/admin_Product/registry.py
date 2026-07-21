# coding: utf-8
# 📂 apps/admin_Product/registry.py

import apps.admin_Product.routes as product_routes

# بيانات الموديول للظهور في الشريط الجانبي
MODULE_NAME = "إدارة المنتجات"
MODULE_ICON = "fa-boxes"
SHOW_IN_SUPPLIER = False

# هنا المفتاح هو الـ endpoint (اسم المسار)، والقيمة هي النص العربي الذي سيظهر في القائمة
LINKS = {
    "admin_product_bp.manage_products": "المنتجات",
    "admin_product_bp.add_product": "إضافة منتج"
    # زر المزامنة سيبقى داخل نافذة إدارة المنتجات (Modal) ولا يظهر هنا
}

def register_module(app):
    # تسجيل الـ Blueprint من ملف routes
    app.register_blueprint(product_routes.admin_product_bp)
