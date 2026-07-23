# coding: utf-8
# 📂 apps/suppliers_product/registry.py

"""
تسجيل تطبيق منتجات الموردين في المنصة
"""

from flask import Blueprint, url_for

# ✅ بيانات الموديول
MODULE_NAME = "منتجاتي"
MODULE_ICON = "fas fa-boxes"
SHOW_IN_SUPPLIER = True

# ✅ الروابط
LINKS = {
    'suppliers_product_bp.products': '📦 منتجاتي',
    'suppliers_product_bp.add_product_page': '➕ إضافة منتج'  # ✅ أضف هذا
}

# ✅ تعريف الـ Blueprint
suppliers_product_bp = Blueprint(
    'suppliers_product_bp',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/suppliers_product/static'
)


def register_module(app):
    """تسجيل الموديول في التطبيق"""
    try:
        from apps.suppliers_product.suppliers_product_routes import suppliers_product_bp as bp
        
        if 'suppliers_product_bp' not in app.blueprints:
            app.register_blueprint(bp, url_prefix='/supplier')
            print("✅ [Registry]: تم تسجيل 'suppliers_product' بنجاح.")
            
    except ImportError as e:
        print(f"❌ [Registry]: خطأ في استيراد suppliers_product_routes: {e}")
    except Exception as e:
        print(f"❌ [Registry]: خطأ في تسجيل suppliers_product: {e}")
    
    return app


# ... باقي الدوال (get_module_stats, get_module_link, get_dashboard_card) ...
