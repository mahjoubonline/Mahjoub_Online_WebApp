from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# تهيئة الأدوات الأساسية
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ربط الأدوات بالتطبيق
    db.init_app(app)
    login_manager.init_app(app)
    
    # إعدادات الحماية والدخول
    login_manager.login_view = 'admin_panel.admin_login' # المسار الافتراضي لمنع المتسللين
    login_manager.login_message_category = 'info'

    # تحميل النماذج (Models) لضمان بناء الجداول
    from core.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # تسجيل البوابات (Blueprints) - ربط الخيوط الثلاثة
    from core.main.routes import main_bp
    from admin_panel.routes import admin_panel as admin_bp
    from supplier_panel.routes import supplier_bp
    
    # تفعيل المسارات في المتصفح
    app.register_blueprint(main_bp) # الواجهة العامة (بدون سابقة)
    app.register_blueprint(admin_bp, url_prefix='/admin-central') # برج الرقابة
    app.register_blueprint(supplier_bp, url_prefix='/supplier-portal') # بوابة الموردين

    return app
