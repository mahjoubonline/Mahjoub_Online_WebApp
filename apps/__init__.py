# coding: utf-8
# 🏗️ مصنع التطبيق المركزي (Application Factory) - منصة محجوب أونلاين 2026

from flask import Flask
from config import Config
from werkzeug.middleware.proxy_fix import ProxyFix
from apps.extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 🔐 تهيئة التشفير
    try:
        from apps.utils.security import cipher_suite
        app.cipher = cipher_suite
    except Exception as e:
        print(f"⚠️ تحذير: فشل تحميل نظام التشفير: {e}")

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_blueprint.login' 

    with app.app_context():
        try:
            # 1. استيراد الموديلات
            from apps.models.admin_db import AdminUser
            from apps.models.supplier_db import Supplier
            from apps.models.wallet_db import SupplierWallet, WalletTransaction
            from apps.models.settlements_db import AdminSettlement
            from apps.models.statement_db import SupplierStatement 
            
            db.create_all() 

            @login_manager.user_loader
            def load_user(user_id):
                return AdminUser.query.get(int(user_id))

            # 2. استيراد وتسجيل البلوبرينتس
            # تأكد أن الأسماء (add_supplier) تطابق ما هو معرف داخل كل ملف routes.py
            from apps.auth_portal.routes import auth_blueprint
            from apps.admin_dashboard.routes import admin_dashboard
            from apps.add_supplier.routes import add_supplier as add_supplier_bp 
            from apps.financial_ops.routes import financial_blueprint 
            from apps.statement.routes import statement_blueprint

            # تسجيل المسارات
            app.register_blueprint(auth_blueprint, url_prefix='/auth')
            app.register_blueprint(admin_dashboard) # الـ Dashboard الأساسي
            app.register_blueprint(add_supplier_bp, url_prefix='/suppliers')
            app.register_blueprint(financial_blueprint, url_prefix='/finance')
            app.register_blueprint(statement_blueprint, url_prefix='/statement')
            
            print("✅ تم تسجيل جميع البلوبرينتس بنجاح.")

        except Exception as e:
            print(f"❌ خطأ فادح أثناء تهيئة التطبيق: {e}")
            # في حال حدوث خطأ هنا، الـ Dashboard لن تظهر!

    return app
