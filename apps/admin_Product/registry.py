# 📂 apps/admin_Product/registry.py

# نستخدم الاستيراد النسبي للوصول إلى البلوبرينت المعرف في routes.py
from .routes import admin_product_bp

# إعدادات العرض في النظام الديناميكي
# هذه البيانات هي التي ستغذي القائمة الجانبية (Sidebar) لاحقاً
MODULE_NAME = "إدارة المنتجات"
MODULE_ICON = "fas fa-box-open"

# روابط الموديول التي ستظهر في القائمة الجانبية
LINKS = {
    "قائمة المنتجات": "admin_product.manage_products",
    "إضافة منتج": "admin_product.add_product"
}

def register_module(app):
    """
    تسجيل موديول 'إدارة المنتجات' في النظام المركزي.
    يقوم بربط البلوبرينت (Blueprint) بالمسار المخصص له.
    """
    try:
        # تسجيل البلوبرينت تحت المسار الرئيسي /admin/products
        # مما يجعل الروابط تصبح /admin/products/ و /admin/products/add وهكذا
        app.register_blueprint(admin_product_bp, url_prefix='/admin/products')
        
        print(f"✅ [Registry]: تم تسجيل موديول 'إدارة المنتجات' بنجاح على المسار (/admin/products).")
    
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول 'إدارة المنتجات': {e}")
