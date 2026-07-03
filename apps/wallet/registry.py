# coding: utf-8
# 📂 apps/wallet/registry.py

from apps.wallet.routes import wallet_bp

# إعدادات الموديول للظهور في لوحة التحكم "القيادة المركزية"
MODULE_NAME = "الرقابة المالية"
MODULE_ICON = "fas fa-wallet"

# الروابط التي تربط القائمة الجانبية بـ routes.py
LINKS = {
    "إدارة المحافظ": "wallet_app.dashboard"
}

def register_module(app):
    """
    تسجيل الموديول وربط الـ Blueprint الخاص به.
    """
    app.register_blueprint(wallet_bp, url_prefix='/wallet')
    print("✅ [Registry]: تم تسجيل موديول 'Wallet' بنجاح.")
