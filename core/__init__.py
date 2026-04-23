from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# تعريف كائن قاعدة البيانات
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, 
                template_folder='../static/templates', # حسب هيكل مجلداتك
                static_folder='../static')
    
    # تحميل الإعدادات من ملف config.py
    app.config.from_object(Config)
    
    # تهيئة قاعدة البيانات مع التطبيق
    db.init_app(app)
    
    # تسجيل الـ Blueprints (الأجزاء المختلفة للمشروع)
    # ملاحظة: تأكد من وجود هذه الملفات داخل مجلداتها
    from admin_panel.routes import admin_bp
    from supplier_panel.routes import supplier_bp
    from webhooks.routes import webhooks_bp
    
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(supplier_bp, url_prefix='/supplier')
    app.register_blueprint(webhooks_bp, url_prefix='/webhooks')
    
    # صفحة رئيسية بسيطة للتأكد من عمل السيرفر
    @app.route('/')
    def index():
        return "<h1>Mahjoub Online System is Running!</h1>"

    return app
