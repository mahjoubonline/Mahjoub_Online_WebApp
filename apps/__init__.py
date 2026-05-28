# coding: utf-8
# 🏗️ مصنع التطبيق المركزي (Application Factory) - منصة محجوب أونلاين 2026

from flask import Flask
from config import Config
from werkzeug.middleware.proxy_fix import ProxyFix
from apps.extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 🔐 تهيئة التشفير مع حماية من الانهيار
    try:
        from apps.utils.security import cipher_suite
        app.cipher = cipher_suite
    except Exception as e:
        print(f"⚠️ تحذير: نظام التشفير غير متاح حالياً: {e}")

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_blueprint.login' 

    with app.app_context():
        try:
            # 1. استيراد الموديلات الأساسية
            from apps.models.admin_db import AdminUser
            from apps.models.supplier_db import Supplier
            from apps.models.wallet_db import SupplierWallet, WalletTransaction
            from apps.models.settlements_db import AdminSettlement
            from apps.models.statement_db import SupplierStatement 
            
            db.create_all() 

            @login_manager.user_loader
            def load_user(user_id):
                return AdminUser.query.get(int(user_id))

            # 2. آلية تسجيل آمنة (Safe Registration)
            # هذه الدالة تضمن أن فشل تسجيل بلوبرينت واحد لا يوقف النظام بالكامل
            def safe_register(blueprint, url_prefix=None):
                try:
                    if url_prefix:
                        app.register_blueprint(blueprint, url_prefix=url_prefix)
                    else:
                        app.register_blueprint(blueprint)
                    print(f"✅ تم تسجيل: {blueprint.name}")
                except Exception as e:
                    print(f"⚠️ فشل تسجيل البلوبرينت {blueprint.name}: {e}")

            # استيراد البلوبرينتس
            from apps.auth_portal.routes import auth_blueprint
            from apps.admin_dashboard.routes import admin_dashboard
            from apps.add_supplier.routes import add_supplier as add_supplier_bp
            from apps.financial_ops.routes import financial_blueprint 
            from apps.statement.routes import statement_blueprint

            # تسجيل كل مسار على حدة
            safe_register(auth_blueprint, '/auth')
            safe_register(admin_dashboard)        # هذه هي الـ Dashboard
            safe_register(add_supplier_bp, '/suppliers')
            safe_register(financial_blueprint, '/finance')
            safe_register(statement_blueprint, '/statement')
            
            print("🚀 تم تشغيل محرك منصة محجوب أونلاين بنجاح.")

        except Exception as e:
            print(f"❌ خطأ فادح في هيكلية التطبيق: {e}")

    return app
