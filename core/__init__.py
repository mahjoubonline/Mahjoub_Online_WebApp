from flask import Flask
from config import Config
from .models import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # تهيئة قاعدة البيانات مع التطبيق
    db.init_app(app)

    # استدعاء الموديولات (Blueprints) بشكل رشيق عند الحاجة
    with app.app_context():
        # هنا سيتم استدعاء لوحات التحكم لاحقاً
        # from admin_panel.routes import admin_bp
        # from supplier_panel.routes import supplier_bp
        
        # تسجيل الموديولات
        # app.register_blueprint(admin_bp, url_prefix='/admin')
        # app.register_blueprint(supplier_bp, url_prefix='/supplier')

        # إنشاء الجداول في قاعدة البيانات إذا لم تكن موجودة
        db.create_all()

    return app
