# coding: utf-8
# 📂 apps/suppliers_dashboard/registry.py

from apps.suppliers_dashboard.routes import suppliers_dashboard_bp

# 1. إعدادات الموديول للظهور
MODULE_NAME = "لوحة التحكم"
MODULE_ICON = "fas fa-tachometer-alt"

# 2. هذا المتغير هو الذي يجعله يظهر في قائمة المورد الجانبية (نظام العزل)
SHOW_IN_SUPPLIER = True

# 3. الروابط (تأكد أن الـ endpoint يطابق الاسم المعرف في Blueprint)
LINKS = {
    "الرئيسية": "suppliers_dashboard.dashboard"
}

def register_module(app):
    """
    تسجيل موديول لوحة تحكم المورد في النظام
    """
    try:
        # تسجيل الـ Blueprint الخاص بلوحة التحكم
        app.register_blueprint(suppliers_dashboard_bp, url_prefix='/supplier/dashboard')
        print("✅ [Registry]: تم تسجيل موديول 'لوحة التحكم' بنجاح.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول 'suppliers_dashboard': {e}")
