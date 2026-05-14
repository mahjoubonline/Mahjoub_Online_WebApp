# coding: utf-8
# 🛡️ المحرك المركزي لمنصة محجوب أونلاين
# التوثيق: هذا الملف هو "المصنع" الذي يبني التطبيق ويجمع كافة المكتبات والأقسام

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect  # درع الحماية ضد الهجمات الإلكترونية

# 1. تهيئة المحركات البرمجية (خارج الدالة لضمان توفرها عالمياً)
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    """
    دالة إنشاء التطبيق (App Factory)
    تقوم بتجميع كافة القطع البرمجية لتشغيل المنصة
    """
    app = Flask(__name__)

    # 2. الإعدادات السيادية للمنصة
    # تأكد من إضافة هذه المتغيرات في إعدادات Railway
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mahjoub_key_2026')
    
    # معالجة رابط قاعدة البيانات ليتوافق مع PostgreSQL في Railway
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///mahjoub_admin.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 3. ربط المحركات بالتطبيق الفعلي
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app) # تفعيل درع الحماية CSRF الذي أضفته في requirements

    # إعدادات نظام تسجيل الدخول
    login_manager.login_view = 'auth_bp.login'
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى هذه المنطقة السيادية."

    # 4. تسجيل الأقسام البرمجية (Blueprints)
    # ملاحظة: نقوم بالاستيراد هنا لتجنب التعارضات البرمجية
    from apps.auth_portal.routes import auth_bp
    from apps.admin_dashboard.routes import admin_dashboard
    from apps.add_supplier.routes import admin_suppliers
    
    # ربط الأقسام بالموقع مع تحديد مسار البداية لكل منها
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_dashboard, url_prefix='/admin')
    app.register_blueprint(admin_suppliers, url_prefix='/admin/suppliers')

    # 5. إنشاء الجداول تلقائياً (بما يتوافق مع سياسة استقرار النظام)
    with app.app_context():
        try:
            # استيراد الموديلات لضمان رؤية قاعدة البيانات لها
            from apps.models.admin_db import AdminUser
            from apps.models.supplier_db import Supplier
            db.create_all()
            print("✅ تم فحص وإنشاء جداول قاعدة البيانات بنجاح.")
        except Exception as e:
            print(f"⚠️ تنبيه: تعذر إنشاء الجداول تلقائياً: {e}")

    return app
