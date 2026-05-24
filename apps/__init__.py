# coding: utf-8
from flask import Flask
from apps.extensions import db, login_manager
from config import Config
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app():
    """
    دالة المصنع (Application Factory) لإنشاء تطبيق Flask وتأمين بواباته.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # 🚀 معالجة الـ Proxy لبيئات الإنتاج (Railway) لمنع تفكك الجلسة وحلقة التوجيه
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    # تهيئة الإضافات المركزية
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_portal.login' 

    @login_manager.user_loader
    def load_user(user_id):
        from apps.models.admin_db import AdminUser
        return AdminUser.query.get(int(user_id))

    # 📥 استدعاء وحدة التحديثات المستقلة وتشغيلها داخل سياق التطبيق فوراً
    with app.app_context():
        from apps.models import wallet_db  # لتنبيه SQLAlchemy بوجود الموديلات
        from apps.migrator import run_db_updates
        run_db_updates()  # تشغيل الهجرة الصامتة بأمان

    # تسجيل الـ Blueprints السيادية
    from apps.auth_portal import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from apps.admin_dashboard import admin_dashboard
    app.register_blueprint(admin_dashboard, url_prefix='/admin')
    
    from apps.add_supplier import admin_suppliers_bp
    app.register_blueprint(admin_suppliers_bp, url_prefix='/suppliers')
    
    from apps.wallet import wallet_blueprint
    app.register_blueprint(wallet_blueprint, url_prefix='/wallet')

    return app
