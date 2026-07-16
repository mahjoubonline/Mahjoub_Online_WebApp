# 📂 apps/admin_platform_treasury/registry.py
from .routes import treasury_bp

MODULE_NAME = "الرقابة المالية"
MODULE_ICON = "fas fa-wallet"

LINKS = {
    "treasury_bp.dashboard": "كشف حساب المنصة",
    "wallet_app.dashboard": "محفظة الموردين" # ربطنا الـ Endpoint الصحيح
}

def register_module(app):
    try:
        app.register_blueprint(treasury_bp, url_prefix='/treasury')
        print("✅ [Registry]: تم تسجيل موديول 'الخزينة' بنجاح.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول الخزينة: {e}")
