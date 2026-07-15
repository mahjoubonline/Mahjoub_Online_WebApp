# 📂 apps/admin_Product/registry.py

from .routes import admin_product_bp

MODULE_NAME = "إدارة المنتجات"
MODULE_ICON = "fas fa-box-open"

# التعديل: قمنا بترك الرابطين كما هما، لأننا برمجنا المسارين في routes.py 
# ليؤديا إلى نفس الصفحة الآمنة (manage_products)
LINKS = {
    "قائمة المنتجات": "admin_product.manage_products",
    "إضافة منتج": "admin_product.add_product"
}

def register_module(app):
    """
    تسجيل موديول 'إدارة المنتجات' في النظام المركزي.
    """
    try:
        # تسجيل البلوبرينت تحت المسار الرئيسي /admin/products
        app.register_blueprint(admin_product_bp, url_prefix='/admin/products')
        
        print(f"✅ [Registry]: تم تسجيل موديول 'إدارة المنتجات' بنجاح على المسار (/admin/products).")
    
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول 'إدارة المنتجات': {e}")
