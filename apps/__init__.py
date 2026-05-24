# coding: utf-8
from flask import Flask
from apps.extensions import db, login_manager
from config import Config
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # حماية المسارات في بيئة الإنتاج
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    # تهيئة الإضافات
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_portal.login'

    with app.app_context():
        # 1. استيراد الموديلات داخل السياق لكسر حلقة الاستيراد
        from apps.models.admin_db import AdminUser
        from apps.models.supplier_db import Supplier
        from apps.models.wallet_db import SupplierWallet, WalletTransaction
        from apps.models.settlements_db import AdminSettlement
        
        @login_manager.user_loader
        def load_user(user_id):
            return AdminUser.query.get(int(user_id))

        # 2. استيراد وتسجيل البلوبرينتس (Routes)
        from apps.auth_portal.routes import auth_blueprint
        from apps.admin_dashboard.routes import admin_dashboard
        from apps.add_supplier.routes import admin_suppliers_bp
        # استيراد البلوبرينت بعد التعديل في __init__.py الخاص بمجلد wallet
        from apps.wallet.routes import wallet_blueprint

        app.register_blueprint(auth_blueprint, url_prefix='/auth')
        app.register_blueprint(admin_dashboard)
        app.register_blueprint(admin_suppliers_bp, url_prefix='/suppliers')
        # تسجيل البلوبرينت الخاص بالمحفظة مع تحديد بادئة المسار
        app.register_blueprint(wallet_blueprint, url_prefix='/wallet')

    return app

# نقطة التشغيل الرئيسية
app = create_app()
