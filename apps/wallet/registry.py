# coding: utf-8
# 📂 apps/wallet/registry.py

from apps.wallet.routes import wallet_bp

def register_module(app):
    """
    هذه الدالة هي التي يبحث عنها ملف apps/__init__.py 
    للقيام بالتسجيل التلقائي للموديول.
    """
    app.register_blueprint(wallet_bp, url_prefix='/wallet')
    print("✅ [Registry]: تم تسجيل موديول 'Wallet' بنجاح.")
