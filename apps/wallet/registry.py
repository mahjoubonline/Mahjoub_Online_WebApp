# coding: utf-8
# 📂 apps/wallet/registry.py

from flask import Blueprint
from apps.wallet.routes import wallet_bp  # تأكد من استيراد البلوبرينت الصحيح

def register_wallet_module(app):
    """
    دالة تسجيل موديول المحفظة في التطبيق الرئيسي.
    """
    
    # تسجيل البلوبرينت الخاص بالمحفظة
    # نربط موديول المحفظة بالمسار (/wallet)
    app.register_blueprint(wallet_bp, url_prefix='/wallet')
    
    # يمكنك إضافة أي تهيئة إضافية هنا (مثل تسجيل Context Processors)
    @app.context_processor
    def inject_wallet_tools():
        return dict(wallet_active=True)

    print("✅ [Registry]: تم تسجيل موديول 'Wallet' بنجاح على المسار (/wallet).")
