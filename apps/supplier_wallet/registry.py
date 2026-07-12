# coding: utf-8
# 📂 apps/suppliers_wallet/registry.py

# لاحظ تغيير كلمة supplier_wallet إلى suppliers_wallet لتطابق اسم المجلد
from apps.suppliers_wallet.routes import supplier_wallet_bp

# 1. إعدادات الموديول
MODULE_NAME = "محفظة المورد"
MODULE_ICON = "fas fa-wallet"

# 2. إظهار في القائمة
SHOW_IN_SUPPLIER = True

# 3. الروابط
LINKS = {
    "supplier_wallet.view_my_wallet": "محفظتي"
}

def register_module(app):
    try:
        # تسجيل الـ Blueprint
        app.register_blueprint(supplier_wallet_bp, url_prefix='/supplier/wallet')
        print("✅ [Registry]: تم تسجيل موديول 'محفظة المورد' بنجاح.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول 'suppliers_wallet': {e}")
