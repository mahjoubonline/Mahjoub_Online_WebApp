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

    # تهيئة الإضافات بربطها بالتطبيق الحالي
    db.init_app(app)
    login_manager.init_app(app)
    
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

    # 💳 استيراد محرك الحوكمة المالية والمحافظ المحدث
    from apps.wallet import admin_wallet

    # ⚙️ تسجيل وعزل المسارات برمجياً لضمان استقرار المنصة بالكامل
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(admin_dashboard_blueprint, url_prefix='/admin')
    
    # 📦 تسجيل محرك الموردين السيادي بمسار مخصص يطابق طلبات الـ Fetch في الواجهة
    app.register_blueprint(admin_suppliers, url_prefix='/admin/suppliers')

    # 💰 تسجيل محرك المحافظ والعمليات المادية الثلاثية في النواة
    app.register_blueprint(admin_wallet)

    # 🚀 الحقل السيادي المضمون: خلق الجداول مسبقاً داخل سياق التطبيق الآمن
    with app.app_context():
        try:
            # استدعاء الموديلات الماليّة لكي يراها محرك SQLAlchemy ويحقنها في الـ Postgres
            from apps.models.wallet_db import Wallet, WalletTransaction
            db.create_all()
            print("✅ تم فحص وتأمين وجود جداول المحافظ المالية في Postgres بنجاح!")
        except Exception as e:
            app.logger.error(f"⚠️ تنبيه حوكمي أثناء فحص جداول قاعدة البيانات: {str(e)}")

    return app
