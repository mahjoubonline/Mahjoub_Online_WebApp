# coding: utf-8
# 📂 apps/__init__.py - المصنع الرئيسي المحمي والمحصن للتطبيق

import os
from flask import Flask, redirect, url_for
from config import Config
from werkzeug.middleware.proxy_fix import ProxyFix
from apps.extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 🛡️ إعداد ProxyFix لضبط البروتوكولات والـ IPs في بيئة Render
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    
    # تهيئة الإضافات الأساسية
    db.init_app(app)
    login_manager.init_app(app)
    
    # تصحيح مسار الدخول الإداري
    login_manager.login_view = 'auth_portal.login' 

    with app.app_context():
        # 1. تهيئة قاعدة البيانات مع معالجة الأخطاء
        try:
            from apps.models.admin_db import AdminUser
            from apps.models.supplier_db import Supplier
            from apps.models.wallet_db import SupplierWallet, WalletTransaction
            from apps.models.settlements_db import AdminSettlement
            from apps.models.statement_db import SupplierStatement
            db.create_all()
        except Exception as e:
            print(f"❌ [Database Error] فشل تهيئة قاعدة البيانات: {e}")

        # 2. تهيئة لودر المستخدم
        @login_manager.user_loader
        def load_user(user_id):
            try:
                return AdminUser.query.get(int(user_id))
            except:
                return None

        # 3. تسجيل المسارات (Blueprints)
        blueprints = [
            ('apps.auth_portal.routes', 'auth_portal', ''), 
            ('apps.add_supplier.routes', 'add_supplier', '/suppliers'),
            ('apps.financial_ops.routes', 'financial_blueprint', '/financial_ops'),
            ('apps.statement.routes', 'statement_blueprint', '/statement'),
            ('apps.admin_dashboard.routes', 'admin_dashboard', '/admin'),
            ('api.webhook', 'webhook_bp', '')
        ]

        for module_path, bp_name, prefix in blueprints:
            try:
                module = __import__(module_path, fromlist=[bp_name])
                blueprint = getattr(module, bp_name)
                app.register_blueprint(blueprint, url_prefix=prefix)
            except Exception as e:
                print(f"⚠️ [Warning] فشل تسجيل {bp_name}: {e}")
        
        # 4. توجيه المسارات الأمنية (إعادة توجيه الجذر للمسار السري)
        @app.route('/')
        def root_redirect():
            # سحب المسار السري من المتغيرات البيئية أو استخدام الافتراضي
            secret_path = os.environ.get('ADMIN_LOGIN_PATH', '/m7jb_sovereign_hq_v2_99x')
            return redirect(secret_path)

        @app.route('/robots.txt')
        def robots_txt():
            return "User-agent: *\nDisallow: /", 200, {'Content-Type': 'text/plain'}

        # 🛡️ جدار الحماية (Security Headers)
        @app.after_request
        def add_security_headers(response):
            response.headers["X-Robots-Tag"] = "noindex, nofollow, noarchive, nosnippet"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
            return response

    return app

# نقطة التشغيل
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
