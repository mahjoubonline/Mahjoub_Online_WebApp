# coding: utf-8
# 📂 apps/admin_Product/registry.py

import apps.admin_Product.routes as product_routes
import apps.admin_Product.routes_review_products as review_routes  # ✅ أضف هذا

# بيانات الموديول للظهور في الشريط الجانبي
MODULE_NAME = "إدارة المنتجات"
MODULE_ICON = "fa-boxes"
SHOW_IN_SUPPLIER = False

# الروابط التي تظهر في القائمة الجانبية
LINKS = {
    "admin_product_bp.manage_products": "📦 المنتجات",
    "review_bp.review_products": "📋 مراجعة المنتجات",  # ✅ استخدم review_bp
    "admin_product_bp.add_product": "➕ إضافة منتج"
}


def register_module(app):
    """تسجيل موديول إدارة المنتجات"""
    try:
        # ✅ تسجيل admin_product_bp
        if 'admin_product_bp' not in app.blueprints:
            app.register_blueprint(product_routes.admin_product_bp, url_prefix='/admin')
            print("✅ [Registry]: تم تسجيل 'admin_product_bp'")
        else:
            print("ℹ️ [Registry]: 'admin_product_bp' مسجل مسبقاً")
        
        # ✅ تسجيل review_bp
        if 'review_bp' not in app.blueprints:
            app.register_blueprint(review_routes.review_bp, url_prefix='/admin')
            print("✅ [Registry]: تم تسجيل 'review_bp'")
        else:
            print("ℹ️ [Registry]: 'review_bp' مسجل مسبقاً")
            
    except Exception as e:
        print(f"❌ [Registry]: خطأ في تسجيل admin_product: {e}")
    
    return app
