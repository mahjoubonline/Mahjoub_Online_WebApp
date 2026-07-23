# coding: utf-8
# 📂 apps/suppliers_dashboard/registry.py

MODULE_NAME = "لوحة التحكم"
MODULE_ICON = "fas fa-home"
SHOW_IN_SUPPLIER = True

# ✅ جميع الروابط في مكان واحد
LINKS = {
    'suppliers_dashboard.dashboard': '📊 لوحة التحكم',
    'suppliers_wallet.withdraw': '💳 سحب الرصيد',
    'suppliers_settings.settings': '⚙️ إعدادات المتجر',
    'ai_bp.chat': '🤖 المساعد الذكي'
}


def register_module(app):
    """تسجيل جميع Blueprints الخاصة بلوحة التحكم"""
    
    from apps.suppliers_dashboard.dashboard_routes import suppliers_dashboard_bp
    from apps.suppliers_dashboard.settings_routes import settings_bp
    from apps.suppliers_dashboard.wallet_routes import wallet_bp
    from apps.suppliers_dashboard.ai_routes import ai_bp
    
    # ✅ تسجيل كل Blueprint على حدة
    if 'suppliers_dashboard' not in app.blueprints:
        app.register_blueprint(suppliers_dashboard_bp, url_prefix='/supplier')
        print("✅ [Registry]: تم تسجيل 'suppliers_dashboard'")
    
    if 'suppliers_settings' not in app.blueprints:
        app.register_blueprint(settings_bp, url_prefix='/supplier')
        print("✅ [Registry]: تم تسجيل 'suppliers_settings'")
    
    if 'suppliers_wallet' not in app.blueprints:
        app.register_blueprint(wallet_bp, url_prefix='/supplier')
        print("✅ [Registry]: تم تسجيل 'suppliers_wallet'")
    
    if 'ai_bp' not in app.blueprints:
        app.register_blueprint(ai_bp, url_prefix='/supplier')
        print("✅ [Registry]: تم تسجيل 'ai_bp'")
    
    return app
