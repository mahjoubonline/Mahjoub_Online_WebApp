# coding: utf-8
# 📂 apps/wallet/registry.py

from apps.wallet.routes import wallet_bp

# بيانات تعريف الموديول للنظام الديناميكي
MODULE_NAME = "الرقابة المالية"
MODULE_ICON = "fas fa-wallet"

# الروابط التي ستظهر تحت هذا الموديول في القائمة الجانبية
LINKS = {
    "خزينة المنصة": "treasury_bp.index",
    "محفظة الموردين": "wallet_app.dashboard"
}

def register_module(app):
    """
    هذه الدالة هي التي يبحث عنها ملف apps/__init__.py 
    للقيام بالتسجيل التلقائي للموديول.
    """
    app.register_blueprint(wallet_bp, url_prefix='/wallet')
    print("✅ [Registry]: تم تسجيل موديول 'Wallet' بنجاح.")
