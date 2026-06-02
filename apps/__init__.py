# coding: utf-8
# 📂 apps/__init__.py - المصنع الرئيسي للتطبيق
# هذا الملف يدير تهيئة التطبيق، الإضافات، الجداول، والمسارات بطريقة آمنة.

from flask import Flask, redirect
from config import Config
from werkzeug.middleware.proxy_fix import ProxyFix
from apps.extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 🛡️ إعداد ProxyFix (ضروري لـ Render لضبط البروتوكولات والـ IP)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    
    # تهيئة الإضافات الأساسية
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_portal.login' 

    with app.app_context():
        # --- استيراد محلي (داخل الـ Context فقط) لكسر الحلقة الدائرية ---
        from apps.models.admin_db import AdminUser
        from apps.models.supplier_db import Supplier
        from apps.models.wallet_db import Wallet, WalletTransaction
        from apps.models.settlements_db import AdminSettlement
        from apps.models.statement_db import SupplierStatement
        
        # إنشاء الجداول تلقائياً
        db.create_all()
        print("⚡ [Database] تم بناء الجداول ومزامنتها بنجاح.")

        # تهيئة user_loader داخل الـ Context
        @login_manager.user_loader
        def load_user(user_id):
            if user_id is not None:
                return AdminUser.query.get(int(user_id))
            return None

        # --- استيراد المسارات (Blueprints) محلياً ---
        from apps.auth_portal.routes import auth_blueprint
        from apps.add_supplier.routes import add_supplier as add_supplier_bp
        from apps.financial_ops.routes import financial_blueprint
        from apps.statement.routes import statement_blueprint
        from apps.admin_dashboard.routes import admin_dashboard

        # تسجيل المسارات
        app.register_blueprint(auth_blueprint, url_prefix='')
        app.register_blueprint(add_supplier_bp, url_prefix='/suppliers')
        app.register_blueprint(financial_blueprint, url_prefix='/financial_ops')
        app.register_blueprint(statement_blueprint, url_prefix='/statement')
        app.register_blueprint(admin_dashboard, url_prefix='/admin')
        
        # توجيه المسار الرئيسي
        @app.route('/')
        def root_redirect():
            return redirect('/login')

    return app
