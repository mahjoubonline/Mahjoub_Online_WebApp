# 📂 apps/admin_platform_treasury/registry.py

from .routes import treasury_bp # تأكد من الاستيراد الصحيح

MODULE_NAME = "الرقابة المالية"
MODULE_ICON = "fas fa-wallet"

LINKS = {
    "treasury_bp.dashboard": "لوحة الخزينة"  # يجب أن يطابق اسم الـ Blueprint المعرف في routes.py
}

def register_module(app):
    try:
        app.register_blueprint(treasury_bp, url_prefix='/treasury')
        print("✅ [Registry]: تم تسجيل موديول 'treasury_bp' بنجاح.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول الخزينة: {e}")
