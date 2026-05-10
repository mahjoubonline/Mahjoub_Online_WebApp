# core/__init__.py
from flask import Flask
from .extensions import db, login_manager # استدعاء الموحدين من الإضافات

def create_app():
    # 1. تهيئة التطبيق وتحديد مسارات الواجهة
    app = Flask(__name__, 
                static_folder='../static', 
                template_folder='../templates')
    
    # 2. تحميل الإعدادات السيادية
    app.config.from_object('config.Config')
    
    # 3. ربط الإضافات (التفعيل الرسمي للترسانة)
    db.init_app(app)
    login_manager.init_app(app)
    
    # إعدادات الحماية (تم نقلها هنا لضمان عملها داخل التطبيق)
    login_manager.login_view = 'admin.login'
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى الترسانة السيادية"
    login_manager.login_message_category = "info"

    with app.app_context():
        # 4. تسجيل المخططات (Models) لضمان ظهورها في القاعدة
        from .models.user import User
        from .models.supplier import Supplier
        
        # 5. تعميد الجداول (الإنشاء التلقائي)
        db.create_all()
        
        # 6. تسجيل لوحة تحكم الإدارة (Blueprint)
        try:
            from admin_panel import admin_bp
            app.register_blueprint(admin_bp) 
            print("✅ تم تسجيل لوحة التحكم بنجاح.")
        except ImportError as e:
            print(f"⚠️ خطأ في تسجيل لوحة التحكم: {e}")

        # 7. محرك استعادة الهوية (Multi-Entity Loader)
        @login_manager.user_loader
        def load_user(user_id):
            if user_id is None or user_id == 'None':
                return None
            
            # البحث أولاً في المسؤولين (الأولوية للقيادة)
            user = User.query.get(int(user_id))
            if user:
                return user
                
            # ثم البحث في الموردين
            return Supplier.query.get(int(user_id))

    return app
