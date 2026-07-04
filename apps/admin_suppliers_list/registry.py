# coding: utf-8
# 📂 apps/admin_suppliers_list/registry.py

# استيراد الـ Blueprint الصحيح من ملف routes
from .routes import suppliers_bp

# إعدادات العرض في الشريط الجانبي
MODULE_NAME = "إدارة الموردين"
MODULE_ICON = "fa-users"

# دمج جميع روابط الموردين هنا ليكون هذا الموديول هو المرجع الرئيسي
LINKS = {
    "قائمة الموردين": "suppliers_bp.list_suppliers",
    "إضافة مورد جديد": "suppliers_bp.add_supplier"
}

def register_module(app):
    """
    تسجيل الـ Blueprint في التطبيق مع معالجة الأخطاء
    """
    try:
        # تم ضبط المسار على /admin/suppliers ليتوافق مع هيكلية لوحة التحكم
        app.register_blueprint(suppliers_bp, url_prefix='/admin/suppliers')
        print("✅ [Registry]: تم تسجيل موديول 'admin_suppliers_list' بنجاح.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول 'admin_suppliers_list': {e}")
