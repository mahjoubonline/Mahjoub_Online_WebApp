from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

# تعريف الإضافات خارج المصنع
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # تهيئة الإضافات مع التطبيق
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.login_view = 'admin.admin_login'

    with app.app_context():
        # استيراد البلوبرنت الخاصة بالإدارة والموردين فقط
        from admin_panel.routes import admin_bp
        # من هنا يمكنك إضافة بلوبرنت الموردين لاحقاً
        
        # تسجيل البلوبرنت
        app.register_blueprint(admin_bp, url_prefix='/admin')

        # توجيه الرابط الرئيسي للموقع إلى لوحة تحكم الإدارة مباشرة
        @app.route('/')
        def index():
            return redirect(url_for('admin.admin_login'))

        return app
