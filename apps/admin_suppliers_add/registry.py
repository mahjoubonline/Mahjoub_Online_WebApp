# coding: utf-8
# 📂 apps/admin_suppliers_add/registry.py

from apps.admin_suppliers_add.routes import admin_suppliers_add_bp

# إعدادات الموديول (تم إبقاء البيانات هنا لغرض التسجيل البرمجي، ولكن لن تظهر في القائمة)
MODULE_NAME = "إدارة الموردين"
MODULE_ICON = "fa-user-plus"

# ✅ التعديل الجوهري: تفريغ الروابط هنا سيمنع ظهور هذا الموديول في القائمة الجانبية
# وبذلك تختفي النسخة المكررة في الشريط الجانبي
LINKS = {}

def register_module(app):
    """
    دالة تسجيل الموديول في التطبيق الرئيسي
    تعمل هذه الدالة على تسجيل الـ Blueprint لضمان عمل الصفحات والمسارات
    """
    try:
        app.register_blueprint(admin_suppliers_add_bp, url_prefix='/admin/suppliers')
        print("✅ [Registry]: تم تسجيل موديول 'admin_suppliers_add' بنجاح (مخفي من القائمة).")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول 'admin_suppliers_add': {e}")
