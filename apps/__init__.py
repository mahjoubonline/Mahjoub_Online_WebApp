from flask import Flask
import os
# تأكد أن المسار يبدأ بـ .models ليعرف بايثون أنه داخل حزمة apps
from .models.admin_db import db  

def create_app():
    app = Flask(__name__)
    
    # الإعدادات السيادية للمنصة
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'mahjoub_online_2026_key'
    
    # معالجة رابط قاعدة البيانات ليتوافق مع Railway (PostgreSQL)
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///mahjoub_admin.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # تهيئة قاعدة البيانات مع التطبيق
    db.init_app(app)

    # استيراد وتسجيل المحركات (Blueprints) باستخدام الاستيراد النسبي
    from .auth_portal.routes import auth_bp
    from .admin_dashboard.routes import admin_dashboard # تأكد من وجود .routes إذا لزم الأمر
    from .add_supplier.routes import admin_suppliers
    
    # تسجيل البوابات الرقمية في هيكل النظام
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_dashboard, url_prefix='/admin')
    app.register_blueprint(admin_suppliers, url_prefix='/admin/suppliers')

    # إنشاء الجداول إذا لم تكن موجودة (مفيد جداً في بيئة Production)
    with app.app_context():
        db.create_all()

    return app
