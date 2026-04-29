import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

# تحميل متغيرات البيئة من ملف .env (للتطوير المحلي)
load_dotenv()

# تعريف الكائنات الأساسية للمنصة
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # --- إعدادات الحوكمة والربط بقاعدة البيانات ---
    # تصحيح رابط قاعدة البيانات ليتوافق مع SQLAlchemy 2.0 في بيئة Render
    database_url = os.getenv("DATABASE_URL")
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "Mahjoub_Smart_Market_2026")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # مبادرة الكائنات مع تطبيق Flask
    db.init_app(app)
    login_manager.init_app(app)
    
    # تحديد صفحة تسجيل الدخول الافتراضية للشركاء
    login_manager.login_view = 'supplier_panel.supplier_login'
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى لوحة التحكم"

    # --- حل مشكلة الاستيراد (Circular Import & ModuleNotFoundError) ---
    with app.app_context():
        # استيراد البلوبرينتس من المسارات الصحيحة كما في هيكلية مشروعك
        try:
            from admin_panel.routes import admin_bp
            from supplier_panel.routes import supplier_bp
            
            # تسجيل بوابات المنصة
            app.register_blueprint(admin_bp, url_prefix='/admin')
            app.register_blueprint(supplier_bp, url_prefix='/supplier')
            
            # استيراد الموديلات لضمان جاهزية قاعدة البيانات
            from . import models
            
        except ImportError as e:
            print(f"خطأ في استيراد الوحدات البرمجية: {e}")

    return app

# دالة تحميل المستخدم لنظام الجلسات (Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    # استيراد موديل المستخدم من المسار الصحيح داخل مجلد models
    from core.models.user import User
    return User.query.get(int(user_id))
