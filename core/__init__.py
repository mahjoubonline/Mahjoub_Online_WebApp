from flask import Flask
from flask_login import LoginManager
from config import Config
from flask_sqlalchemy import SQLAlchemy

# تعريف الكائنات المركزية (دون ربطها بالتطبيق بعد)
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # إنشاء كائن التطبيق
    app = Flask(__name__, 
                static_folder='../static', 
                template_folder='../templates')
    
    # تحميل الإعدادات من ملف Config
    app.config.from_object(Config)
    
    # ربط المحركات بالكائن المخصص للتطبيق
    db.init_app(app)
    login_manager.init_app(app)
    
    # إعدادات حارس البوابة (Login Manager)
    login_manager.login_view = 'admin_panel.login'
    login_manager.login_message = "هذه المنطقة تتطلب تعميداً سيادياً للدخول."
    login_manager.login_message_category = "info"

    with app.app_context():
        # استيراد الموديلات داخل سياق التطبيق لضمان تسجيل الجداول
        from core.models import User

        @login_manager.user_loader
        def load_user(user_id):
            # البحث عن المستخدم في الجدول الموحد
            return User.query.get(int(user_id))

        # 🚨 كسر حلقة الاستيراد: يتم استيراد البوابات هنا بعد إنشاء كائن db
        try:
            from admin_panel import admin_bp
            from supplier_panel import supplier_bp
            
            # تسجيل البوابات بمساراتها الفرعية
            app.register_blueprint(admin_bp, url_prefix='/admin')
            app.register_blueprint(supplier_bp, url_prefix='/supplier')
            
            print("✅ [System] تم كسر حلقة الاستيراد وربط البوابات السيادية بنجاح.")
        except Exception as e:
            print(f"❌ [Critical Error] فشل في ربط البوابات: {e}")

    return app
