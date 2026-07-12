# coding: utf-8
# 📂 apps/supplier_wallet/registry.py

from apps.suppliers_wallet.routes import supplier_wallet_bp

# 1. إعدادات الموديول للظهور
MODULE_NAME = "محفظة المورد"
MODULE_ICON = "fas fa-wallet"

# 2. هذا المتغير هو الذي يجعله يظهر في قائمة المورد الجانبية (نظام العزل)
SHOW_IN_SUPPLIER = True

# 3. الروابط: تم تصحيح الترتيب (اسم المسار أولاً ثم النص الظاهر)
# ليتطابق مع المنطق المستخدم في نظام القائمة الجانبية لديك
LINKS = {
    "supplier_wallet.view_my_wallet": "محفظتي"
}

def register_module(app):
    """
    تسجيل الموديول في النظام
    """
    try:
        # تسجيل الـ Blueprint الخاص بمحفظة المورد
        app.register_blueprint(supplier_wallet_bp, url_prefix='/supplier/wallet')
        print("✅ [Registry]: تم تسجيل موديول 'محفظة المورد' بنجاح.")
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول 'supplier_wallet': {e}")
