from flask import Flask
from flask_login import LoginManager
from config import Config
from flask_sqlalchemy import SQLAlchemy

# 1. تعريف الكائنات المركزية
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, 
                static_folder='../static', 
                template_folder='../templates')
    
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    login_manager.login_view = 'admin_panel.login'
    login_manager.login_message = "هذه المنطقة تتطلب تعميداً سيادياً للدخول."
    login_manager.login_message_category = "info"

    with app.app_context():
        # استيراد الموديلات
        from core.models import User

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        # 🚨 التعديل هنا: نستخدم الاستيراد المباشر من الكائن لضمان المسار
        try:
            # استيراد كائنات البلوبرنت من ملفات الـ __init__ الخاصة بالمجلدات
            from admin_panel import admin_bp
            from supplier_panel import supplier_bp
            
            # تسجيل البوابات
            app.register_blueprint(admin_bp, url_prefix='/admin')
            app.register_blueprint(supplier_bp, url_prefix='/supplier')
            
            print("✅ [System] تم توحيد المحرك وربط البوابات بنجاح.")
        except Exception as e:
            # هذا السطر سيطبع لك السبب الدقيق للخطأ في الـ Logs
            print(f"❌ [Critical Error] فشل في ربط البوابات السيادية: {e}")

    return app
