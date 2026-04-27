import os
from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# 1. تعريف الكائنات الأساسية (النواة السيادية)
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    # 2. إنشاء كائن التطبيق
    app = Flask(__name__)

    # 3. الإعدادات السيادية (Configurations)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mahjoub_online_9046_sovereign_key')
    
    # ربط قاعدة البيانات
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///mahjoub_online.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 4. تهيئة الإضافات مع التطبيق
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # إعدادات نظام الدخول الذكي
    # ملاحظة: سنترك login_view مرناً ونستخدم دالة مخصصة للتوجيه
    login_manager.login_view = 'supplier_panel.login'
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى النطاق المطلوب."
    login_manager.login_message_category = "info"

    # دالة مخصصة لإعادة التوجيه بناءً على الرابط المطلوب
    @login_manager.unauthorized_handler
    def unauthorized():
        # إذا كان المستخدم يحاول دخول لوحة الإدارة، وجهه لصفحة دخول الإدارة
        if request.path.startswith('/admin_control_9046'):
            return redirect(url_for('admin_panel.admin_login'))
        # غير ذلك، وجهه لصفحة دخول الموردين
        return redirect(url_for('supplier_panel.login'))

    # 5. تسجيل البوابات (Blueprints) داخل سياق التطبيق
    with app.app_context():
        # استيراد النماذج لضمان بناء الجداول
        from core import models
        
        # أ: تسجيل بوابة الموردين (Supplier Panel)
        from supplier_panel import supplier_bp
        app.register_blueprint(supplier_bp, url_prefix='/supplier')

        # ب: تسجيل بوابة الإدارة (Admin Panel) - مركز القيادة المستقل
        try:
            from admin_panel import admin_bp
            app.register_blueprint(admin_bp, url_prefix='/admin_control_9046')
        except ImportError:
            print("تنبيه: مجلد admin_panel غير موجود أو يحتوي على خطأ.")

        # إنشاء الجداول
        db.create_all()

    return app

# 6. إنشاء نسخة التطبيق النهائية
app = create_app()

@login_manager.user_loader
def load_user(user_id):
    from core.models import User
    return User.query.get(int(user_id))
