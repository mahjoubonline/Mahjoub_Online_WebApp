# coding: utf-8
# 📂 apps/admin_suppliers_list/registry.py

# استيراد الـ Blueprint من ملف routes الخاص بهذا الموديول
from .routes import suppliers_bp

# إعدادات العرض في الشريط الجانبي
MODULE_NAME = "قائمة الشركاء"
MODULE_ICON = "fa-users"

# ✅ الربط تحت المظلة الرئيسية "إدارة الموردين"
# ملاحظة: تأكد أن اسم الـ Blueprint (الاسم داخل Blueprint('اسم_الـ_بلوبرنت', ...))
# هو المستخدم في الـ url_for أدناه، وليس اسم المتغير suppliers_bp
LINKS = {
    "إدارة الموردين": {
        "قائمة الشركاء": "suppliers.list_suppliers"
    }
}

def register_module(app):
    """
    تسجيل الـ Blueprint في التطبيق
    """
    try:
        app.register_blueprint(suppliers_bp, url_prefix='/admin/suppliers')
        print("✅ [Registry]: تم تسجيل موديول 'admin_suppliers_list' بنجاح.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول 'admin_suppliers_list': {e}")
