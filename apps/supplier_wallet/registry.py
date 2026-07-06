# coding: utf-8
# 📂 apps/supplier_wallet/registry.py

from .routes import supplier_wallet_bp

def register_module(app):
    try:
        # تأكد هنا أنك لا تعطي اسم 'suppliers_orders_portal' كمعامل لـ register_blueprint
        # يجب أن يكون الاسم فريداً أو لا يتم تمريره ليأخذ اسم الـ Blueprint الافتراضي
        app.register_blueprint(supplier_wallet_bp, url_prefix='/suppliers/wallet')
        
        if not hasattr(app, 'registered_modules'):
            app.registered_modules = {}
            
        app.registered_modules['supplier_wallet_portal'] = MODULE_INFO
        
        print("✅ [Registry]: تم تسجيل موديول 'supplier_wallet' بنجاح.")
    except Exception as e:
        print(f"🚨 [Registry Error]: {e}")

MODULE_INFO = {
    "display_name": "المحفظة المالية",
    "icon": "fas fa-wallet",
    "show_in_supplier": True,
    "links": {
        "كشف الحساب": "supplier_wallet.view_my_wallet"
    }
}
