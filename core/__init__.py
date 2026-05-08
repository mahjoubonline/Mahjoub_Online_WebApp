from flask import Flask
from flask_login import LoginManager
from .extensions import db  # استدعاء db من الهيكلية المعتمدة للنظام

# إعداد مدير تسجيل الدخول لضمان أمان مركز القيادة السيادي
login_manager = LoginManager()

def create_app():
    # 1. تهيئة التطبيق مع تحديد مسارات القوالب والملفات الثابتة العامة
    app = Flask(__name__, 
                static_folder='../static', 
                template_folder='../templates')
    
    # 2. تحميل الإعدادات من ملف Config السيادي (قاعدة البيانات، المفاتيح السرية)
    app.config.from_object('config.Config')
    
    # 3. ربط الإضافات (Extensions) بالتطبيق
    db.init_app(app)
    login_manager.init_app(app)
    
    # تحديد صفحة تسجيل الدخول الافتراضية للتحويل التلقائي
    login_manager.login_view = 'admin.login'
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى الترسانة السيادية"
    login_manager.login_message_category = "info"

    with app.app_context():
        # 4. استدعاء الموديلات (Models) لضمان تسجيل الجداول في النواة
        from .models.user import User
        from .models.supplier import Supplier
        
        # 5. تعميد الجداول (Database Synchronization)
        # سيقوم بإنشاء الجداول المفقودة تلقائياً
        db.create_all()
        
        # 6. تسجيل لوحة تحكم "محجوب أونلاين" (Blueprint Registration)
        try:
            from admin_panel import admin_bp
            # تسجيل البلوبرينت مع التأكد من عزل المسارات
            app.register_blueprint(admin_bp) 
        except ImportError as e:
            print(f"⚠️ Warning: Admin Panel could not be registered. Error: {e}")

        # 7. بروتوكول استعادة المستخدم الذكي (Multi-Entity User Loader)
        # هذا المحرك يتعرف على الهوية سواء كان داخلاً كـ "مدير" أو "مورد"
        @login_manager.user_loader
        def load_user(user_id):
            # أولاً: البحث في جدول الإدارة والمستخدمين
            user = User.query.get(int(user_id))
            if user:
                return user
            # ثانياً: إذا لم يوجد، البحث في جدول الموردين (للسماح لهم بدخول لوحاتهم مستقبلاً)
            return Supplier.query.get(int(user_id))

    return app
