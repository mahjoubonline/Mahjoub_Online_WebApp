# coding: utf-8
# 📂 apps/admin_platform_treasury/registry.py

from apps.admin_platform_treasury.routes import treasury_bp

# ✅ قم بحذف أو تعليق هذا السطر لإخفاء "الخزينة" من القائمة الرئيسية
# MODULE_NAME = "الخزينة" 
# MODULE_ICON = "fa-vault"

# تأكد أن LINKS فارغ أيضاً
LINKS = {} 

def register_module(app):
    """
    تسجيل موديول الخزينة برمجياً فقط (لتعمل الروابط) 
    دون إظهار أي شيء في الشريط الجانبي.
    """
    try:
        app.register_blueprint(treasury_bp, url_prefix='/admin/treasury')
        print("✅ [Registry]: تم تسجيل موديول 'Admin Platform Treasury' بنجاح (مخفي من القائمة).")
    except Exception as e:
        print(f"❌ [Registry Error]: {e}")
