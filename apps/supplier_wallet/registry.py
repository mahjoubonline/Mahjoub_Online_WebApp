# coding: utf-8
# 📂 apps/supplier_wallet/registry.py

from apps.supplier_wallet.routes import supplier_wallet_bp

def register_supplier_wallet_module(app):
    """
    دالة تقوم بتسجيل موديول محفظة المورد في التطبيق الأساسي
    يتم استدعاؤها عند تهيئة التطبيق.
    """
    # نقوم بتسجيل الـ Blueprint الخاص بالمورد مع بادئة (Prefix) محددة
    # ليتمكن المورد من الدخول عبر الرابط: /supplier/wallet/...
    app.register_blueprint(supplier_wallet_bp, url_prefix='/supplier/wallet')
    
    print("✅ تم تسجيل موديول 'محفظة المورد' بنجاح.")
