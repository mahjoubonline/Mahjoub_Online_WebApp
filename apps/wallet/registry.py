# coding: utf-8
# 📂 apps/wallet/registry.py

from apps.wallet.routes import wallet_bp

# إعدادات الموديول
MODULE_NAME = "الرقابة المالية"
MODULE_ICON = "fas fa-wallet"

# ✅ الحل: تفريغ الروابط هنا سيمنع ظهور هذا الموديول كعنصر مستقل في القائمة الجانبية
LINKS = {}

def register_module(app):
    """
    تسجيل الموديول برمجياً فقط (لضمان عمل المسارات)
    دون إظهاره في القائمة الجانبية.
    """
    try:
        app.register_blueprint(wallet_bp, url_prefix='/wallet')
        print("✅ [Registry]: تم تسجيل موديول 'Wallet' بنجاح (مخفي من القائمة).")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول 'Wallet': {e}")
