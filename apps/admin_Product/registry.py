# coding: utf-8
# 📂 apps/admin_Product/registry.py

# 1. البيانات التعريفية للظهور في الشريط الجانبي (Sidebar)
MODULE_NAME = "إدارة المنتجات"
MODULE_ICON = "fas fa-boxes"
SHOW_IN_SUPPLIER = False  # لكي يظهر في لوحة القيادة المركزية للآدمن وليس للموردين

# 2. قائمة الروابط الفرعية داخل الموديول
# المفتاح هو Endpoint الـ Blueprint، والقيمة هي الاسم الظاهر في القائمة
LINKS = {
    "admin_product_bp.manage_products": "قائمة المنتجات",
    "admin_product_bp.add_product": "إضافة منتج",
}

# 3. دالة التسجيل الآلي لتسجيل الـ Blueprint داخل Flask App
def register_module(app):
    """
    تستدعيها دالة create_app في apps/__init__.py تلقائياً عند إقلاع التطبيق
    """
    try:
        from apps.admin_Product.routes import admin_product_bp
        app.register_blueprint(admin_product_bp)
        print("✅ [Registry]: تم تسجيل موديول إدارة المنتجات بنجاح.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل Blueprint لموديول المنتجات: {e}")
