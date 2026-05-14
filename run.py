# coding: utf-8
import os
from flask import Flask, redirect, url_for
from models.admin_db import db  # استيراد كائن قاعدة البيانات المركزي

def create_app():
    """
    دالة بناء وتجهيز تطبيق محجوب أونلاين السيادي
    """
    # تحديد مسار القوالب (Templates) لضمان القراءة الصحيحة
    app = Flask(__name__, template_folder='apps/templates')
    
    # إعداد مفتاح الأمان للتشفير والجلسات
    app.secret_key = os.environ.get('SECRET_KEY') or 'MAHJOUB_SECURE_2026'

    # معالجة رابط قاعدة البيانات ليتوافق مع Railway (PostgreSQL)
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        # تصحيح البروتوكول من postgres إلى postgresql
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    # ربط قاعدة البيانات سواء كانت SQLite للتطوير أو Postgres للإنتاج
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///mahjoub_admin.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # تهيئة قاعدة البيانات مع التطبيق
    db.init_app(app)

    # تسجيل البلوبرينت (المصانع البرمجية) لتفعيل الروابط
    from apps.auth_portal.routes import auth_bp
    from apps.admin_dashboard.routes import admin_dashboard  
    from apps.add_supplier.routes import admin_suppliers

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_dashboard, url_prefix='/admin')
    app.register_blueprint(admin_suppliers, url_prefix='/admin/suppliers')

    # إنشاء الجداول تلقائياً عند بدء التشغيل إذا لم تكن موجودة
    with app.app_context():
        db.create_all()

    # توجيه الرابط الرئيسي للمنصة مباشرة إلى صفحة تسجيل الدخول
    @app.route('/')
    def root():
        return redirect(url_for('auth_portal.login')) 

    return app

# تعريف المتغير 'app' في المستوى العام ليتمكن Gunicorn من رؤيته (إصلاح انهيار Railway)
app = create_app()

if __name__ == '__main__':
    # تحديد المنفذ ديناميكياً بناءً على بيئة الاستضافة
    port = int(os.environ.get('PORT', 8080))
    # تشغيل الخادم على العنوان 0.0.0.0 ليكون متاحاً عبر الإنترنت
    app.run(host='0.0.0.0', port=port)
