# coding: utf-8
from flask import Flask
from apps.extensions import db, login_manager
from config import Config
from apps.models.admin_db import AdminUser

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # تهيئة الإضافات
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_portal.login'

    # دالة تعريف المستخدم (حل نهائي لخطأ Missing user_loader)
    @login_manager.user_loader
    def load_user(user_id):
        return AdminUser.query.get(int(user_id))

    # تسجيل البلوبرينتس (النوافذ المستقلة)
    from apps.auth_portal import auth_blueprint
    from apps.admin_dashboard import admin_dashboard_bp
    from apps.add_supplier import admin_suppliers_bp
    from apps.wallet import wallet_bp

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(admin_dashboard_bp, url_prefix='/admin')
    app.register_blueprint(admin_suppliers_bp, url_prefix='/suppliers')
    app.register_blueprint(wallet_bp, url_prefix='/wallet')

    return app
