import os
import sys
from flask import Flask
from flask_login import LoginManager
from config import Config
from flask_sqlalchemy import SQLAlchemy

# تعريف الكائنات المركزية
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # إعداد المسارات لضمان العمل على Linux/Railway
    base_dir = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, '..'))
    
    # إضافة جذر المشروع لمسار النظام لضمان رؤية البوابات
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    app = Flask(__name__, 
                static_folder=os.path.join(project_root, 'static'), 
                template_folder=os.path.join(project_root, 'templates'))
    
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    login_manager.login_view = 'supplier_panel.login'
    login_manager.login_message = "هذه المنطقة تتطلب تعميداً سيادياً للدخول."
    login_manager.login_message_category = "info"

    with app.app_context():
        from core.models import User

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        # ربط البوابات السيادية
        try:
            from admin_panel import admin_bp
            from supplier_panel import supplier_bp
            
            app.register_blueprint(admin_bp, url_prefix='/admin')
            app.register_blueprint(supplier_bp, url_prefix='/supplier')
            
            print("✅ [System] تم توحيد المحرك وربط البوابات بنجاح.")
        except Exception as e:
            print(f"❌ [Critical Error] فشل في ربط البوابات: {str(e)}")

    return app
