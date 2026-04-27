import os
import sys
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import Config

# تعريف الكائنات المركزية
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # الحصول على المسار المطلق للمجلد الحالي (core) والمجلد الرئيسي (Root)
    base_dir = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, '..'))

    # 🚨 أهم خطوة: إضافة مجلد المشروع لمسار النظام لضمان رؤية admin_panel و supplier_panel
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

    with app.app_context():
        # استيراد الموديلات من مجلدها الجديد
        from core.models import User

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        # تسجيل البوابات (Blueprints)
        try:
            from admin_panel import admin_bp
            from supplier_panel import supplier_bp
            
            app.register_blueprint(admin_bp, url_prefix='/admin')
            app.register_blueprint(supplier_bp, url_prefix='/supplier')
            
            print("✅ [System] تم ربط البوابات السيادية بنجاح.")
        except Exception as e:
            print(f"❌ [Critical Error] فشل الربط: {e}")

    return app
