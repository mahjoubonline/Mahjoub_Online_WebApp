# 📂 apps/suppliers_wallet/registry.py
from apps.suppliers_wallet.routes import supplier_wallet_bp

MODULE_NAME = "محفظة المورد"
MODULE_ICON = "fas fa-wallet"
SHOW_IN_SUPPLIER = True

# تأكد أن المفتاح هو الـ Endpoint والقيمة هي الاسم
LINKS = {
    "supplier_wallet.view_my_wallet": "محفظتي"
}

def register_module(app):
    app.register_blueprint(supplier_wallet_bp, url_prefix='/supplier/wallet')
    print("✅ [Registry]: تم تسجيل موديول 'محفظة المورد' بنجاح.")
