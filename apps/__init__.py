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

    # 📥 استدعاء الموديلات وتجهيزها داخل سياق التطبيق فوراً عند الإقلاع
    with app.app_context():
        # استدعاء الموديلات لتسجيل الجداول في قاعدة البيانات
        from apps.models import admin_db
        from apps.wallet import models
        
        # إنشاء الجداول تلقائياً إذا لم تكن موجودة
        db.create_all()

        # تسجيل الـ Blueprint الخاص بالمحافظ والتسويات المطور
        from apps.wallet import wallet_blueprint
        app.register_blueprint(wallet_blueprint, url_prefix='/wallet')

    # إرجاع كائن التطبيق (هذا السطر حاسم ومحاذاته يجب أن تكون تابعة للدالة create_app ليعمل المصنع)
    return app
