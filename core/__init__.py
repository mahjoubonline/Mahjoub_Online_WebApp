from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# تهيئة قاعدة البيانات
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='../templates') # المجلد العام للقوالب
    
    # إعدادات السيرفر السيادية
    app.config['SECRET_KEY'] = 'mahjoub_online_secret_key_2026'
    # استخدام SQLite كبداية، ويمكن تغييره لـ PostgreSQL عند الرفع الفعلي
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mahjoub_online.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ربط الإضافات بالتطبيق
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin_panel.login' # الصفحة الافتراضية عند محاولة الدخول غير المصرح
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى قمرة القيادة"

    # تسجيل الـ Blueprints (ربط الأقسام ببعضها)
    
    # 1. ربط لوحة الإدارة المركزية
    from admin_panel import admin_panel as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    # 2. ربط بوابة شركاء النجاح (الموردين)
    from supplier_panel import supplier_panel as supplier_blueprint
    app.register_blueprint(supplier_blueprint, url_prefix='/supplier')

    # تهيئة جداول قاعدة البيانات عند التشغيل الأول
    with app.app_context():
        from core import models
        db.create_all()

    return app

# تعريف كيفية جلب المستخدم (سواء كان أدمن أو مورد)
@login_manager.user_loader
def load_user(user_id):
    from core.models import User, Supplier
    # يحاول النظام البحث في جدول الأدمن أولاً، ثم الموردين
    user = User.query.get(int(user_id))
    if user:
        return user
    return Supplier.query.get(int(user_id))
