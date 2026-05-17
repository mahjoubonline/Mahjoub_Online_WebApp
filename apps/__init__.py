# apps/__init__.py
# coding: utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# استيراد ملف الإعدادات الخاص بهيكل تطبيقك الحالي (عدّل المسار حسب اسم ملفك إن كان مختلفاً)
from config import Config 

# 1️⃣ أولاً: إنشاء الكائنات الأساسية وتصديرها للذاكرة
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # 2️⃣ ثانياً: تحميل إعدادات السيرفر وقاعدة البيانات أولاً وقبل أي شيء!
    # هذا السطر يمنع ظهور خطأ RuntimeError ويحقن الـ URI داخل الـ app
    app.config.from_object(Config)

    # 3️⃣ ثالثاً: ربط الكائنات مع التطبيق بعد أن أصبحت الإعدادات محقونة وجاهزة
    db.init_app(app)
    login_manager.init_app(app)

    # -------------------------------------------------------------------------
    # 4️⃣ رابعاً: استدعاء وتسجيل المسارات والبلوبرينتس في الأسفل بعد استقرار النواة
    # -------------------------------------------------------------------------
    
    # استدعاء موديل الموردين ليكون مرئياً لقاعدة البيانات
    from apps.models.supplier_db import Supplier

    # تسجيل البلوبرينت الخاص بإضافة الموردين لـ "منصة محجوب أونلاين"
    from apps.add_supplier.routes import admin_suppliers
    app.register_blueprint(admin_suppliers, url_prefix='/admin/suppliers')

    # 🛡️ اترك بقية تسجيلات الـ Blueprints القديمة الخاصة بـ Dashboard تطبيقك هنا:
    # from apps.base import blueprint
    # app.register_blueprint(blueprint)

    return app
