# coding: utf-8
from flask import Flask
from apps.extensions import db, login_manager
from config import Config
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # معالجة الـ Proxy لبيئات الإنتاج
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    db.init_app(app)
    login_manager.init_app(app)
    # ربط بوابة الدخول (تأكد أن الاسم هو ما تم تعريفه في الـ Blueprint)
    login_manager.login_view = 'auth_portal.login' 

    @login_manager.user_loader
    def load_user(user_id):
        from apps.models.admin_db import AdminUser
        return AdminUser.query.get(int(user_id))

    with app.app_context():
        # 1. بوابة المحافظ
        from apps.wallet import wallet_blueprint
        app.register_blueprint(wallet_blueprint, url_prefix='/wallet')

        # 2. بوابة المصادقة (Auth)
        from apps.auth_portal.routes import auth_blueprint
        app.register_blueprint(auth_blueprint, url_prefix='/auth')

        # 3. لوحة التحكم
        from apps.admin_dashboard.routes import admin_dashboard_blueprint
        app.register_blueprint(admin_dashboard_blueprint)

        db.create_all()

    return app

# تشغيل المصنع
app = create_app()
