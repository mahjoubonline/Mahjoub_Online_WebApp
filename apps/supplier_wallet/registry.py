# coding: utf-8
# 📂 apps/supplier_wallet/registry.py

from apps.supplier_wallet.routes import supplier_wallet_bp

# 1. إعدادات الموديول
MODULE_NAME = "محفظة المورد"
MODULE_ICON = "fas fa-wallet"
SHOW_IN_SUPPLIER = True

# 2. الروابط: ملاحظة: يجب أن يتطابق 'supplier_wallet' مع الاسم 
# المعرف داخل Blueprint('supplier_wallet', __name__) في ملف routes.py
LINKS = {
    "محفظتي": "supplier_wallet.index"
}

def register_module(app):
    """
    تسجيل الموديول في النظام مع تأمين الروابط
    """
    try:
        # تسجيل الـ Blueprint
        app.register_blueprint(supplier_wallet_bp, url_prefix='/supplier/wallet')
        
        # للتحقق من الأخطاء: طباعة الـ Endpoints المسجلة
        print("✅ [Registry]: تم تسجيل موديول 'محفظة المورد' بنجاح.")
        print(f"🔗 الـ Blueprint المسجل هو: {supplier_wallet_bp.name}")
        
    except Exception as e:
        print(f"❌ [Registry Error]: فشل تسجيل موديول 'supplier_wallet': {e}")
