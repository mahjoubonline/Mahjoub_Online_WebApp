# coding: utf-8
# 🛡️ المحرك المركزي لمنصة محجوب أونلاين 2026
# التوثيق: المصنع الرئيسي (App Factory) الذي يدير الدروع الأمنية وقاعدة البيانات

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# 1. تهيئة المحركات البرمجية (Global Instances)
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    """
    دالة إنشاء التطبيق (App Factory)
    تقوم بتجميع كافة القطع البرمجية لتشغيل المنصة تحت مظلة أمنية واحدة
    """
    app = Flask(__name__)

    # 2. الإعدادات السيادية للمنصة
    # يتم سحب المفاتيح الحساسة من بيئة تشغيل Railway لضمان الأمان المطلق
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mahjoub_sovereign_key_2026')
    
    # تحويل رابط PostgreSQL ليتوافق مع مكتبة SQLAlchemy الحديثة
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///mahjoub_admin.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 3. ربط المحركات بالتطبيق الفعلي
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app) # درع الحماية ضد هجمات تزوير الطلبات عبر المواقع

    # إعدادات نظام الولوج
    login_manager.login_view = 'auth_bp.login'
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى هذه المنطقة السيادية."
    login_manager.login_message_category = "info"

    # 4. تسجيل الأقسام البرمجية (Blueprints)
    # الاستيراد داخل الدالة يمنع "الاستيراد الدائري" (Circular Imports)
    from apps.auth_portal.routes import auth_bp
    from apps.admin_dashboard.routes import admin_dashboard
    from apps.add_supplier.routes import admin_suppliers
    
    # ربط المسارات بالهيكل التنظيمي للمنصة
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_dashboard, url_prefix='/admin')
    app.register_blueprint(admin_suppliers, url_prefix='/admin/suppliers')

    # 5. بناء جدار قاعدة البيانات (Database Integrity)
    with app.app_context():
        try:
            # استيراد حزمة النماذج لضمان أن SQLAlchemy يراها عند بناء الجداول
            # هذا السطر يحل مشكلة No module named 'apps.models'
            import apps.models 
            
            db.create_all()
            print("✅ تم فحص وتعميد جداول قاعدة البيانات بنجاح.")
        except Exception as e:
            print(f"⚠️ تنبيه سيادي: حدث خلل أثناء محاولة إنشاء الجداول: {e}")

    return app
