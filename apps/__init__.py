# coding: utf-8
from flask import Flask, redirect
from config import Config
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 🛡️ إعداد ProxyFix (ضروري للعمل خلف بروكسي Render)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    # استيراد db و login_manager داخل الدالة
    from apps.extensions import db, login_manager
    
    # تهيئة الإضافات
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_portal.login' 

    with app.app_context():
        # ✅ التعديل هنا: استيراد النماذج من حزمة models التي تجمعهم جميعاً
        from apps.models import (
            AdminUser, 
            Supplier, 
            Wallet, 
            WalletTransaction, 
            AdminSettlement, 
            SupplierStatement
        )
        
        print("⚡ تم تحميل النماذج بنجاح من apps.models")

        @login_manager.user_loader
        def load_user(user_id):
            return AdminUser.query.get(int(user_id)) if user_id else None

        # تسجيل الـ Blueprints
        def safe_register(blueprint, url_prefix=None):
            try:
                app.register_blueprint(blueprint, url_prefix=url_prefix)
            except Exception as e:
                print(f"⚠️ فشل تسجيل {blueprint.name}: {e}")

        # تسجيل المسارات
        from apps.auth_portal.routes import auth_blueprint
        safe_register(auth_blueprint, url_prefix='')

        from apps.add_supplier.routes import add_supplier as add_supplier_bp
        safe_register(add_supplier_bp, url_prefix='/suppliers')

        from apps.financial_ops.routes import financial_blueprint
        safe_register(financial_blueprint, url_prefix='/finance')

        from apps.statement.routes import statement_blueprint
        safe_register(statement_blueprint, url_prefix='/statement')

        from apps.admin_dashboard.routes import admin_dashboard
        safe_register(admin_dashboard, url_prefix='/admin')
        
        @app.route('/')
        def root_redirect():
            return redirect('/login')

    return app
