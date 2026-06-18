# coding: utf-8
from flask import Flask, redirect, url_for
from flask_talisman import Talisman
from config import Config
from apps.extensions import db, login_manager, migrate

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static', instance_relative_config=True)
    app.config.from_object(Config)

    # 🛡️ سياسة أمان المحتوى (CSP)
    csp_policy = {
        'default-src': ["'self'"],
        'style-src': ["'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com", "https://fonts.googleapis.com", "https://cdn.jsdelivr.net"],
        'script-src': ["'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com", "https://cdn.jsdelivr.net"],
        'font-src': ["'self'", "data:", "https://fonts.gstatic.com", "https://cdnjs.cloudflare.com", "https://cdn.jsdelivr.net"],
        'img-src': ["'self'", "data:", "https://*"],
        'connect-src': ["'self'", "https://mahjoub.online"]
    }
    
    Talisman(app, force_https=True, content_security_policy=csp_policy,
             frame_options='SAMEORIGIN', referrer_policy='strict-origin-when-cross-origin')

    # تهيئة الإضافات
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_portal.login'

    @login_manager.user_loader
    def load_user(user_id):
        from apps.models.admin_db import AdminUser
        return AdminUser.query.get(int(user_id))

    # تسجيل المسارات (Blueprints)
    from apps.auth_portal.routes import auth_portal
    from apps.admin_dashboard.routes import admin_dashboard
    from apps.wallet.routes import wallet_app
    from apps.vault.routes import vault_bp
    from apps.orders.routes import orders_bp  # تم تصحيح الاسم هنا
    from apps.api.webhooks import webhooks_bp

    @app.route('/')
    def index():
        return redirect(url_for('auth_portal.login'))

    app.register_blueprint(auth_portal, url_prefix='/auth')
    app.register_blueprint(admin_dashboard, url_prefix='/admin')
    app.register_blueprint(wallet_app, url_prefix='/wallet')
    app.register_blueprint(vault_bp, url_prefix='/vault')
    app.register_blueprint(orders_bp, url_prefix='/orders')  # تم تصحيح الاسم هنا
    app.register_blueprint(webhooks_bp, url_prefix='/api')

    # إعداد الجداول
    with app.app_context():
        try:
            from apps.models.admin_db import AdminUser
            # تأكد أن هذه الملفات موجودة في المسارات المحددة
            db.create_all() 
            print("✅ [System] تم الاتصال بقاعدة البيانات وإنشاء الجداول بنجاح.")
        except Exception as e:
            print(f"⚠️ [Error] فشل في تهيئة قاعدة البيانات: {e}")

    return app
