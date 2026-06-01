# coding: utf-8
# 🏗️ مصنع التطبيق المركزي (Application Factory) - منصة محجوب أونلاين 2026

from flask import Flask
from config import Config
from werkzeug.middleware.proxy_fix import ProxyFix
from apps.extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 🔐 تهيئة التشفير (تم تعطيل الاستيراد المباشر لتجنب انهيار النظام بسبب نقص المكتبات)
    app.cipher = None 
    print("ℹ️ نظام التشفير: تم تجاوز الاستيراد للحفاظ على استقرار التطبيق.")

    # 🛡️ إعداد ProxyFix لاستقبال النطاقات والشرطات من Vercel بشكل سليم
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_blueprint.login' 

    with app.app_context():
        # دالة تسجيل آمنة تمنع انهيار النظام وتدعم النطاقات الفرعية (Subdomains)
        def safe_register(blueprint, url_prefix=None, subdomain=None):
            try:
                if subdomain:
                    app.register_blueprint(blueprint, subdomain=subdomain)
                elif url_prefix:
                    app.register_blueprint(blueprint, url_prefix=url_prefix)
                else:
                    app.register_blueprint(blueprint)
                print(f"✅ تم تسجيل: {blueprint.name} " + (f"على النطاق الفرعي [{subdomain}]" if subdomain else ""))
            except Exception as e:
                print(f"⚠️ تحذير: فشل تسجيل البلوبرينت {blueprint.name}: {e}")

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
                try:
                    return AdminUser.query.get(int(user_id))
                except:
                    return None

            # 2. استيراد وتسجيل البلوبرينتس (ربط لوحة التحكم بالنطاق الفرعي admin)
            try:
                from apps.auth_portal.routes import auth_blueprint
                # بوابات الدخول والتوثيق تعمل على النطاق الفرعي لضمان الأمان
                safe_register(auth_blueprint, url_prefix='/auth', subdomain='admin')
            except Exception as e:
                print(f"❌ تعذر تحميل auth_blueprint: {e}")

            try:
                from apps.admin_dashboard.routes import admin_dashboard
                # 🚀 توجيه لوحة التحكم الرئيسية لتعمل مباشرة عند فتح admin.mahjoub.online
                safe_register(admin_dashboard, subdomain='admin')
            except Exception as e:
                print(f"❌ تعذر تحميل admin_dashboard: {e}")

            try:
                from apps.add_supplier.routes import add_supplier as add_supplier_bp
                safe_register(add_supplier_bp, url_prefix='/suppliers', subdomain='admin')
            except Exception as e:
                print(f"❌ تعذر تحميل add_supplier: {e}")

            try:
                from apps.financial_ops.routes import financial_blueprint
                safe_register(financial_blueprint, url_prefix='/finance', subdomain='admin')
            except Exception as e:
                print(f"❌ تعذر تحميل financial_blueprint: {e}")

            try:
                from apps.statement.routes import statement_blueprint
                safe_register(statement_blueprint, url_prefix='/statement', subdomain='admin')
            except Exception as e:
                print(f"❌ تعذر تحميل statement_blueprint: {e}")
            
            print("🚀 تم تشغيل محرك المنصة بنجاح وتوزيع النطاقات الفرعية.")

        except Exception as e:
            print(f"❌ خطأ جسيم في تهيئة التطبيق: {e}")

    return app
