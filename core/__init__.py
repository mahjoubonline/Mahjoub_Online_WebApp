import os
from flask import Flask
from flask_login import LoginManager
from config import Config
from flask_sqlalchemy import SQLAlchemy

# 1. تعريف الكائنات المركزية
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # استخدام os.path لضمان أن المسارات تعمل على Railway (Linux) و Windows
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    app = Flask(__name__, 
                static_folder=os.path.join(base_dir, '../static'), 
                template_folder=os.path.join(base_dir, '../templates'))
    
    app.config.from_object(Config)
    
    # ربط المحركات بكائن التطبيق
    db.init_app(app)
    login_manager.init_app(app)
    
    # إعدادات حماية الدخول
    login_manager.login_view = 'supplier_panel.login' # جعلنا الافتراضي بوابة الموردين
    login_manager.login_message = "هذه المنطقة تتطلب تعميداً سيادياً للدخول."
    login_manager.login_message_category = "info"

    with app.app_context():
        # استيراد الموديلات داخل السياق
        from core.models import User

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        # 🚨 تعميد الروابط وربط البوابات
        try:
            # استيراد البلوبرنت من ملفات __init__
            from admin_panel import admin_bp
            from supplier_panel import supplier_bp
            
            # تسجيل البوابات بمسارات واضحة
            # التأكد من عدم وجود تكرار في السلاش /
            app.register_blueprint(admin_bp, url_prefix='/admin')
            app.register_blueprint(supplier_bp, url_prefix='/supplier')
            
            print("✅ [System] تم توحيد المحرك وربط البوابات بنجاح.")
        except Exception as e:
            print(f"❌ [Critical Error] فشل في ربط البوابات: {e}")

    return app
