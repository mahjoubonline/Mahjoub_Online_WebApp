# coding: utf-8
# 📂 apps/supplier_wallet/registry.py

from .routes import supplier_wallet_bp

# متغيرات يتوقعها نظام Auto-Discovery في __init__.py
MODULE_NAME = "المحفظة المالية"
MODULE_ICON = "fas fa-wallet"
LINKS = {
    "كشف الحساب": "supplier_wallet.view_my_wallet"
}

def register_module(app):
    try:
        app.register_blueprint(supplier_wallet_bp, url_prefix='/suppliers/wallet')
        print("✅ [Registry]: تم تسجيل موديول 'supplier_wallet' بنجاح.")
    except Exception as e:
        print(f"🚨 [Registry Error]: {e}")
