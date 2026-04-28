import os
from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix

# 1. تعريف الكائنات الأساسية (خارج create_app لمنع التضارب)
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    # إنشاء تطبيق Flask
    # ملاحظة: تم ضبط template_folder ليشمل المجلدات الخارجية
    app = Flask(__name__)
    
    # حل مشكلة الروابط و البروتوكولات (HTTP/HTTPS) في بيئة Render/Railway
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    # 2. تحميل الإعدادات
    try:
        from config import Config
        app.config.from_object(Config)
    except ImportError:
        # إعدادات احتياطية في حال فقدان ملف config.py
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///mahjoub_online.db'
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'mahjoub-secret-key-123'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 3. تهيئة الإضافات مع التطبيق
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # 4. إعدادات نظام الدخول
    login_manager.login_view = 'admin_panel.admin_login'
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى النظام السيادي."
    login_manager.login_message_category = "info"

    # --- ⚓ الموجه الافتراضي ⚓ ---
    @app.route('/')
    def index():
        # توجيه تلقائي لصفحة الإدارة عند فتح الرابط الرئيسي للموقع
        return redirect(url_for('admin_panel.admin_login'))

    with app.app_context():
        # 5. استيراد الموديلات لبناء قاعدة البيانات
        from core.models.user import User
        from core.models.product import Product
        from core.models.supplier import Supplier
        
        # إنشاء الجداول إذا لم تكن موجودة
        db.create_all() 

        # 6. تسجيل البوابات السيادية (Blueprints)
        # يتم الاستيراد هنا حصراً لتجنب أخطاء الاستيراد الدائري (Circular Import)
        
        try:
            from supplier_panel.routes import supplier_bp
            if 'supplier_panel' not in app.blueprints:
                app.register_blueprint(supplier_bp, url_prefix='/supplier')
            print("✅ تم ربط بوابة الموردين بنجاح")
        except Exception as e:
            print(f"⚠️ خطأ في ربط بوابة الموردين: {e}")

        try:
            from admin_panel.routes import admin_bp 
            if 'admin_panel' not in app.blueprints:
                app.register_blueprint(admin_bp, url_prefix='/admin')
            print("✅ تم ربط برج الرقابة بنجاح")
        except Exception as e:
            print(f"⚠️ خطأ في ربط بوابة الإدارة: {e}")

        # 7. عملية التعميد (تأكيد الحسابات الأساسية فور التشغيل)
        try:
            if not User.query.filter_by(username="علي محجوب").first():
                admin_user = User(username="علي محجوب", role="admin", status="approved")
                admin_user.set_password("123")
                db.session.add(admin_user)
                db.session.commit()
                print("✨ تم تعميد حساب القائد علي محجوب بنجاح")
        except Exception as e:
            db.session.rollback()
            print(f"⚠️ فشل التعميد الآلي: {e}")

    return app

# 8. محمل المستخدم لنظام Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from core.models.user import User
    try:
        return db.session.get(User, int(user_id))
    except:
        return None
