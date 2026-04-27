from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    with app.app_context():
        # استيراد الموديلات
        from core import models
        
        @login_manager.user_loader
        def load_user(user_id):
            from core.models import User
            return User.query.get(int(user_id))

        # تسجيل البوابات (الربط السيادي)
        try:
            from admin_panel import admin_bp
            from supplier_panel import supplier_bp
            
            app.register_blueprint(admin_bp, url_prefix='/admin')
            app.register_blueprint(supplier_bp, url_prefix='/supplier')
            print("✅ [System] تم ربط البوابات بنجاح.")
        except Exception as e:
            print(f"❌ [Critical Error] فشل الربط: {e}")

    return app
