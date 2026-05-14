import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager  # 🛡️ نظام إدارة الدخول السيادي
from models.admin_db import db        # استيراد قاعدة البيانات المركزية

# إعداد مدير الدخول
login_manager = LoginManager()
login_manager.login_view = 'auth_portal.login'  # اسم الدالة التي توجه المستخدم لصفحة تسجيل الدخول
login_manager.login_message = "وصول غير مصرح! يرجى تسجيل الدخول أولاً."
login_manager.login_message_category = "info"

def create_app():
    """
    دالة إنشاء التطبيق وتجهيز كافة المحركات البرمجية
    """
    app = Flask(__name__)
    
    # 1. الإعدادات السيادية للمنصة
    # استخدام مفتاح سري قوي للتشفير وحماية الجلسات
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'mahjoub_online_2026_key'
    
    # 2. معالجة رابط قاعدة البيانات ليتوافق مع البيئات السحابية (Railway/Heroku)
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        # PostgreSQL يتطلب بروتوكول postgresql:// بدلاً من postgres://
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///mahjoub_admin.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 3. تهيئة المحركات مع التطبيق
    db.init_app(app)
    login_manager.init_app(app)

    # 4. إعداد محمل المستخدم (User Loader)
    # هذا الجزء يربط نظام الدخول بقاعدة بيانات المسؤولين
    from models.admin_db import Admin  # افترضنا وجود موديل Admin
    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))

    # 5. استيراد وتسجيل البلوبرينت (Blueprints)
    # ربط الأجزاء المختلفة من التطبيق بالمحرك الرئيسي
    from .auth_portal.routes import auth_bp
    from .admin_dashboard.routes import admin_dashboard
    from .add_supplier.routes import admin_suppliers
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_dashboard, url_prefix='/admin')
    app.register_blueprint(admin_suppliers, url_prefix='/admin/suppliers')

    # 6. إنشاء الجداول تلقائياً في سياق التطبيق
    with app.app_context():
        try:
            db.create_all()
            print("✅ تم فحص وإنشاء جداول قاعدة البيانات بنجاح.")
        except Exception as e:
            print(f"❌ خطأ أثناء إنشاء الجداول: {e}")

    return app
