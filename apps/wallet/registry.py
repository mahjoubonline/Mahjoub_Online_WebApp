# coding: utf-8
# 📂 apps/wallet/registry.py

from apps.wallet.routes import wallet_bp # تأكد أن هذا السطر يعمل

def register_module(app): # يجب أن يكون اسم الدالة register_module
    app.register_blueprint(wallet_bp, url_prefix='/wallet')
    print("✅ [Registry]: تم تسجيل موديول 'Wallet' بنجاح على المسار (/wallet).")
