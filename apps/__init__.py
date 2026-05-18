# coding: utf-8
# 🏢 المصنع المركزي للنواة - منصة محجوب أونلاين 2026

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# إنشاء الكائنات المركزية كنسخ مستقلة لمنع التعارض الدائري
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # تعيين مجلد القوالب العام كخلفية احتياطية للتطبيق كاملاً
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config)

    # 🛡️ التحديث السيادي لعام 2026: حل مشكلة تشفير النصوص العربية (Unicode) في Flask 3+
    # نقوم بحقن ترميز الـ UTF-8 مباشرة في محرك الـ JSON الخاص بـ Flask لضمان طباعة النصوص العربية بنقاء كامل
    app.json.ensure_ascii = False

    # تهيئة الإضافات بربطها بالتطبيق الحالي أولاً
    db.init_app(app)
    login_manager.init_app(app)

    # 🛡️ استدعاء النماذج الحوكمة فوراً بعد التهيئة لإجبار Flask و SQLAlchemy 
    # على تسجيل الجداول وأحداث توليد المعرفات والمحافظ تلقائياً في سياق النواة
    with app.app_context():
        from apps.models import admin_db
        from apps.models import supplier_db
        from apps.models import wallet_db
        print("🛡️ تم تعميد النماذج وإخضاع ملفات قواعد البيانات لسياق الـ SQLAlchemy بنجاح.")
    
    # 🛡️ الحماية السيادية: تحديد المسار الكامل لـ Flask-Login
    login_manager.login_view = 'auth_portal.login'
    login_manager.login_message = 'يرجى إثبات الهوية الرقمية للوصول إلى المنطقة السيادية.'
    login_manager.login_message_category = 'warning'

    # 🔑 تعريف الـ user_loader لجلب الهوية من قاعدة البيانات
    @login_manager.user_loader
    def load_user(user_id):
        from apps.models.admin_db import AdminUser
        return AdminUser.query.get(int(user_id))

    # 📥 استيراد البلوبرينتس الفرعية بشكل آمن ومباشر لمنع التداخل الدائري
    from apps.auth_portal import auth_blueprint
    from apps.admin_dashboard import admin_dashboard_blueprint
    
    # 🎯 الاستيراد الصحيح والنقي مباشرة من مجلد حزمة الموردين المعزولة
    from apps.add_supplier import admin_suppliers

    # 💳 الاستيراد الحاسم والسيادي لمحرك المحافظ من مسار الحزمة التابع لـ routes
    from apps.wallet.routes import admin_wallet

    # ⚙️ تسجيل وعزل المسارات برمجياً لضمان استقرار المنصة بالكامل
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(admin_dashboard_blueprint, url_prefix='/admin')
    
    # 📦 تسجيل محرك الموردين السيادي بمسار مخصص يطابق طلبات الـ Fetch في الواجهة
    app.register_blueprint(admin_suppliers, url_prefix='/admin/suppliers')

    # 💰 تعميد وتسجيل محرك المحافظ والعمليات المادية الثلاثية بشكل رسمي في النواة
    app.register_blueprint(admin_wallet)

    return app
