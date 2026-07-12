# 📂 apps/supplier_wallet/registry.py
# تأكد أن هذا السطر يطابق تماماً اسم المجلد (بدون s)
from apps.supplier_wallet.routes import supplier_wallet_bp

MODULE_NAME = "محفظة المورد"
MODULE_ICON = "fas fa-wallet"
SHOW_IN_SUPPLIER = True

LINKS = {
    "supplier_wallet.view_my_wallet": "محفظتي"
}

def register_module(app):
    app.register_blueprint(supplier_wallet_bp, url_prefix='/supplier/wallet')
