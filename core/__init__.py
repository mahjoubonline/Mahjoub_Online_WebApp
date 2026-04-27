from flask import Flask
from flask_login import LoginManager
from config import Config
from flask_sqlalchemy import SQLAlchemy

# 1. تعريف الكائنات المركزية (المحركات السيادية)
# يجب أن يكون db هنا هو الكائن الوحيد الذي تستورده الموديلات
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # إنشاء كائن التطبيق مع تحديد مسارات الملفات الثابتة والقوالب العامة
    app = Flask(__name__, 
                static_folder='../static', 
                template_folder='../templates')
    
    # تحميل الإعدادات من ملف Config (مثل SQLALCHEMY_DATABASE_URI)
    app.config.from_object(Config)
    
    # 2. ربط المحركات بكائن التطبيق
    db.init_app(app)
    login_manager.init_app(app)
    
    # إعدادات حماية الدخول
    login_manager.login_view = 'admin_panel.login'
    login_manager.login_message = "هذه المنطقة تتطلب تعميداً سيادياً للدخول."
    login_manager.login_message_category = "info"

    with app.app_context():
        # 3. استيراد الموديلات داخل السياق لضمان ربطها بالمحرك db الموحد
        from core.models import User

        @login_manager.user_loader
        def load_user(user_id):
            # البحث في الجدول الموحد (أدمن أو مورد)
            return User.query.get(int(user_id))

        # 4. تسجيل البوابات (Blueprints) 
        # نستخدم الاستيراد المتأخر هنا لكسر حلقة الاستيراد الدائري تماماً
        try:
            from admin_panel import admin_bp
            from supplier_panel import supplier_bp
            
            # تسجيل بوابة الإدارة
            app.register_blueprint(admin_bp, url_prefix='/admin')
            
            # تسجيل بوابة الموردين بمسارها السيادي
            app.register_blueprint(supplier_bp, url_prefix='/supplier')
            
            print("✅ [System] تم توحيد المحرك وربط البوابات بنجاح.")
        except Exception as e:
            print(f"❌ [Critical Error] فشل في ربط البوابات السيادية: {e}")

    return app
