import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config  # استيراد كلاس الإعدادات الذي راجعناه

# تهيئة الإضافات الأساسية للمنصة
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    
    # تحميل الإعدادات من ملف config.py
    # هذا السطر يغنينا عن كتابة الإعدادات يدوياً هنا ويجلب DATABASE_URL و SECRET_KEY
    app.config.from_object(config_class)

    # تفعيل الملحقات داخل التطبيق
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # تحديد صفحة تسجيل الدخول الافتراضية للتحكم السيادي
    login_manager.login_view = 'admin_panel.admin_login'

    with app.app_context():
        # --- تسجيل البوابات (Blueprints) ---
        
        # 1. بوابة الإدارة المركزية (Admin Panel)
        # نستخدم الاستيراد داخل السياق لضمان عدم حدوث تضارب في الأسماء (Circular Import)
        from admin_panel import admin_blueprint
        app.register_blueprint(admin_blueprint, url_prefix='/admin')

        # 2. الواجهة الأمامية للمتجر (Main)
        from core.main import main_bp # تأكد من وجود __init__.py داخل مجلد main
        app.register_blueprint(main_bp)

        # استدعاء الموديلات لضمان بناء الجداول في قاعدة بيانات Railway
        from core.models.user import User
        from core.models.supplier import Supplier
        from core.models.product import Product

    return app

# دالة تحميل المستخدم لمنصة محجوب أونلاين
@login_manager.user_loader
def load_user(user_id):
    from core.models.user import User
    return User.query.get(int(user_id))
