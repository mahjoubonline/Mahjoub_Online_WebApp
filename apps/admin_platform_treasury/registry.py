# 📂 apps/admin_platform_treasury/registry.py

from .routes import treasury_bp

# 1. تحديث الأسماء لتكون أكثر وضوحاً وتوافقاً مع القائمة الجانبية
MODULE_NAME = "الرقابة المالية"
MODULE_ICON = "fas fa-wallet"

# 2. تأكد أن الـ Key هنا يطابق الـ endpoint في @treasury_bp.route(...)
# إذا كان معرف بـ @treasury_bp.route('/dashboard') في ملف routes.py
LINKS = {
    "treasury_bp.dashboard": "كشف حساب المنصة"
}

def register_module(app):
    try:
        # تأكد من أن الـ url_prefix متوافق مع المسارات التي تفتحها في المتصفح
        app.register_blueprint(treasury_bp, url_prefix='/treasury')
        print("✅ [Registry]: تم تسجيل موديول 'الخزينة' بنجاح.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول الخزينة: {e}")
