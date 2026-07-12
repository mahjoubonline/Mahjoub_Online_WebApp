# 📂 apps/suppliers_wallet/registry.py

from apps.suppliers_wallet.routes import supplier_wallet_bp

MODULE_NAME = "محفظة المورد"
MODULE_ICON = "fas fa-wallet"
SHOW_IN_SUPPLIER = True

# التغيير هنا: استخدام اسم الـ blueprint + النقطة + اسم الدالة
# تأكد أن اسم الـ blueprint في routes.py هو 'supplier_wallet'
LINKS = {
    "supplier_wallet.view_my_wallet": "محفظتي"
}

def register_module(app):
    try:
        app.register_blueprint(supplier_wallet_bp, url_prefix='/supplier/wallet')
    except Exception as e:
        print(f"❌ [Registry Error]: {e}")
