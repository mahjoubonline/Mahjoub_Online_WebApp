# coding: utf-8
# 📂 apps/suppliers_dashboard/registry.py

from apps.suppliers_dashboard.routes import dashboard_bp

def register_module(app):
    """
    تسجيل لوحة تحكم المورد (Supplier Dashboard)
    يتم استدعاء هذه الدالة في ملف الـ factory الخاص بالتطبيق.
    """
    try:
        # تسجيل الـ Blueprint مع البادئة '/suppliers'
        # مما يعني أن أي مسار داخل routes.py سيتم الوصول إليه عبر /suppliers/..
        app.register_blueprint(dashboard_bp, url_prefix='/suppliers')
        
        print("✅ [Registry]: تم تسجيل وحدة 'suppliers_dashboard' بنجاح على المسار (/suppliers).")
        
    except Exception as e:
        print(f"🚨 [Registry Error]: فشل تسجيل وحدة لوحة تحكم المورد: {e}")

# إعدادات الموديول الفنية للتوثيق والإدارة
MODULE_CONFIG = {
    "module_name": "suppliers_dashboard",
    "version": "1.0.0",
    "status": "active"
}
