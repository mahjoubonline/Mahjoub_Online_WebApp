import os
from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# تعريف الكائنات الأساسية
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # جلب الإعدادات
    from config import Config
    app.config.from_object(Config)

    # تهيئة الإضافات
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # تحديد صفحة الدخول الافتراضية
    login_manager.login_view = 'admin_panel.admin_login'

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('admin_panel.admin_login'))

    with app.app_context():
        # استيراد النماذج من المجلد الجديد core/models
        from core import models
        
        # --- تسجيل بوابة الموردين (تعمل حالياً ✅) ---
        try:
            from supplier_panel.routes import supplier_bp
            app.register_blueprint(supplier_bp, url_prefix='/supplier')
            print("✅ تم تفعيل بوابة الموردين")
        except Exception as e:
            print(f"⚠️ خطأ في بوابة الموردين: {e}")

        # --- تسجيل بوابة الإدارة (برج الرقابة 🏛️) ---
        try:
            # التعديل الذهبي: الاستيراد من المسار الكامل للملف لضمان العثور على الكائن
            from admin_panel.routes import admin_bp 
            app.register_blueprint(admin_bp, url_prefix='/admin')
            print("✅ تم تفعيل بوابة الإدارة بنجاح")
        except Exception as e:
            # هذا السطر سيطبع لك السبب الدقيق في حال وجود مشكلة أخرى
            print(f"⚠️ فشل تسجيل بوابة الإدارة: {e}")

        db.create_all()

    return app

@login_manager.user_loader
def load_user(user_id):
    # تحديث المسار ليتوافق مع تقسيم الموديلات الجديد
    from core.models.user import User
    try:
        return User.query.get(int(user_id))
    except:
        return None
