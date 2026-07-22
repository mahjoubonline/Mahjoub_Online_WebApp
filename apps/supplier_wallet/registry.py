# coding: utf-8
# 📂 apps/supplier_wallet/registry.py

"""
تسجيل تطبيق محفظة المورد في المنصة
"""

from flask import Blueprint

# ✅ بيانات الموديول
MODULE_NAME = "محفظة المورد"
MODULE_ICON = "fas fa-wallet"
SHOW_IN_SUPPLIER = True

# ✅ الروابط التي تظهر في القائمة الجانبية للمورد
LINKS = {
    "supplier_wallet.view_my_wallet": "💳 محفظتي"
}


# ✅ تعريف الـ Blueprint الرئيسي
supplier_wallet_bp = Blueprint(
    'supplier_wallet',
    __name__,
    template_folder='templates'
)


def register_module(app):
    """
    تسجيل تطبيق محفظة المورد في التطبيق الرئيسي
    """
    # ✅ استيراد الـ routes بعد تعريف الـ Blueprint
    from apps.supplier_wallet import routes
    
    # ✅ تسجيل الـ Blueprint
    if 'supplier_wallet' not in app.blueprints:
        app.register_blueprint(supplier_wallet_bp, url_prefix='/supplier/wallet')
        print("✅ [Registry]: تم تسجيل 'supplier_wallet' بنجاح.")
    
    return app
