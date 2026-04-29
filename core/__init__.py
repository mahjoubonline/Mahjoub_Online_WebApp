import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # تصحيح مسار قاعدة بيانات Render
    db_url = os.getenv("DATABASE_URL", "sqlite:///mahjoub.db")
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "MAHJOUB_2026_KEY")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'supplier_panel.supplier_login'

    with app.app_context():
        # استيراد وتسجيل البوابات المبسطة
        from admin_panel.routes import admin_bp
        from supplier_panel.routes import supplier_bp
        
        app.register_blueprint(admin_bp, url_prefix='/admin')
        app.register_blueprint(supplier_bp, url_prefix='/supplier')

    return app

@login_manager.user_loader
def load_user(user_id):
    from core.models.user import User
    return User.query.get(int(user_id))
