# apps/__init__.py
# coding: utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# استيراد كلاس الإعدادات الرئيسي لتهيئة قاعدة البيانات
from config import Config 

# 1️⃣ أولاً: إنشاء الكائنات الأساسية وتصديرها للذاكرة
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # 2️⃣ ثانياً: تحميل إعدادات السيرفر وقاعدة البيانات (لمنع خطأ RuntimeError)
    app.config.from_object(Config)

    # 3️⃣ ثالثاً: ربط الكائنات مع التطبيق بعد استقرار الإعدادات
    db.init_app(app)
    login_manager.init_app(app)

    # -------------------------------------------------------------------------
    # 4️⃣ رابعاً: منطقة حقن وتسجيل المسارات والـ Blueprints (آمنة ومحمية)
    # -------------------------------------------------------------------------
    
    # [أ] استدعاء الموديلات لتهيئة الجداول في قاعدة البيانات
    from apps.models.supplier_db import Supplier

    # [ب] تسجيل مسار إضافة الموردين الجديد
    from apps.add_supplier.routes import admin_suppliers
    app.register_blueprint(admin_suppliers, url_prefix='/admin/suppliers')

    # 🔑 1. تسجيل مسار بوابة المصادقة وتسجيل الدخول (auth_portal)
    from apps.auth_portal.routes import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # 📊 2. تسجيل مسار لوحة التحكم الرئيسية ومحتواها (admin_dashboard)
    from apps.admin_dashboard.routes import admin_dashboard_blueprint
    app.register_blueprint(admin_dashboard_blueprint, url_prefix='/admin/dashboard')

    # 🏛️ 3. تسجيل مسار الهيكل الأساسي المشترك (templates/admin_base)
    # ملاحظة: إذا كان الـ admin_base يخدم كقوالب عامة (Templates) مشتركة يتم استدعاؤها 
    # عبر الـ extends داخل الـ HTML فلا يحتاج بلوبرينت منفصل، ولكن إذا كان له مسارات خاصة:
    from apps.main_routes import main_blueprint  # أو اسم الملف الذي يدير الواجهات العامة لديك
    app.register_blueprint(main_blueprint)

    return app
