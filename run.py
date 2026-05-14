# coding: utf-8
import os
from flask import Flask, redirect, url_for
from models.admin_db import db  # استيراد قاعدة البيانات المركزية

def create_app():
    """
    دالة بناء وتجهيز تطبيق محجوب أونلاين السيادي
    """
    # تهيئة التطبيق وتحديد مجلد القوالب (Jinja2 Templates)
    app = Flask(__name__, template_folder='apps/templates')
    
    # إعداد مفتاح الأمان (Secret Key) لتشفير الجلسات وحماية البيانات
    app.secret_key = os.environ.get('SECRET_KEY') or 'MAHJOUB_SECURE_2026'

    # معالجة رابط قاعدة البيانات ليتوافق مع Railway (PostgreSQL)
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        # تصحيح البروتوكول ليتوافق مع SQLAlchemy
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    # ربط قاعدة البيانات سواء كانت SQLite للتطوير أو Postgres للإنتاج
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///mahjoub_admin.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # تهيئة قاعدة البيانات لتعمل مع التطبيق
    db.init_app(app)

    # تسجيل المصانع البرمجية (Blueprints) لتفعيل الروابط
    from apps.auth_portal.routes import auth_bp
    from apps.admin_dashboard.routes import admin_dashboard  
    from apps.add_supplier.routes import admin_suppliers

    # تفعيل المسارات في المتصفح
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_dashboard, url_prefix='/admin')
    app.register_blueprint(admin_suppliers, url_prefix='/admin/suppliers')

    # إنشاء الجداول تلقائياً في قاعدة البيانات عند بدء التشغيل
    with app.app_context():
        db.create_all()

    # توجيه الصفحة الرئيسية مباشرة إلى بوابة الدخول
    @app.route('/')
    def root():
        return redirect(url_for('auth_portal.login')) 

    return app

# تعريف المتغير 'app' عالمياً ليتمكن الخادم السحابي من تشغيله (حل مشكلة Crashed)
app = create_app()

if __name__ == '__main__':
    # الحصول على المنفذ (Port) ديناميكياً من الخادم
    port = int(os.environ.get('PORT', 8080))
    # تشغيل التطبيق ليكون متاحاً لجميع الأجهزة
    app.run(host='0.0.0.0', port=port)
