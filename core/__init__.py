from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from sqlalchemy import text

# تعريف الأدوات الأساسية للترسانة
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # تهيئة الإضافات وربطها بالتطبيق
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # تحديد بوابة الدخول الرئيسية للإدارة
    login_manager.login_view = 'admin.admin_login'

    # --- التعديل الجوهري هنا ---
    # استيراد الموديلات من المجلد المركزي لضمان ترتيب بناء الجداول
    from core.models import User, Supplier, Order 
    # ---------------------------
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        try:
            print("🚨 جاري تصفير الترسانة الرقمية وإعادة الهيكلة...")
            
            # تنفيذ مسح شامل للجداول (بالترتيب الصحيح لتجنب تعليق المفاتيح الخارجية)
            # تم إضافة جدول orders لضمان تنظيف كامل
            db.session.execute(text('DROP TABLE IF EXISTS orders CASCADE;'))
            db.session.execute(text('DROP TABLE IF EXISTS suppliers CASCADE;'))
            db.session.execute(text('DROP TABLE IF EXISTS products CASCADE;'))
            db.session.execute(text('DROP TABLE IF EXISTS users CASCADE;'))
            db.session.commit()
            
            # إعادة بناء الهيكل النظيف
            db.create_all() 
            print("✅ تم إعادة بناء الجداول بنظافة تامة.")

            # زرع حساب القائد (علي محجوب) في الهيكل الجديد
            # ملاحظة: تأكد أن موديل User يحتوي على حقول role و is_active_account
            admin_user = User(
                username="علي محجوب", 
                role='admin', 
                is_active_account=True
            )
            admin_user.set_password('123')
            db.session.add(admin_user)
            db.session.commit()
            print("👑 تم زرع حساب القائد بنجاح: علي محجوب / 123")

        except Exception as e:
            db.session.rollback()
            print(f"⚠️ خطأ حرج أثناء التصفير أو الزرع: {e}")

    # تسجيل Blueprint الإدارة لربط مجلد admin_panel بالمنصة
    from admin_panel.routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
