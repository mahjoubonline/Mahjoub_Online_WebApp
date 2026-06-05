# coding: utf-8
# 📂 apps/__init__.py - المصنع المحصن والمحمي (نسخة التصحيح الذاتي)

import os
from datetime import timedelta
from flask import Flask, redirect
from config import Config
from werkzeug.middleware.proxy_fix import ProxyFix
from apps.extensions import db, login_manager
from sqlalchemy import text

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 🛡️ إعدادات الأمان للجلسات
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)
    app.config['SESSION_COOKIE_HTTPONLY'] = True  
    app.config['SESSION_COOKIE_SECURE'] = True    
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    # 🛡️ الحماية من التزييف
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_portal.login' 

    with app.app_context():
        # 🛡️ استيراد النماذج لضمان تسجيل الجداول في db
        from apps.models.admin_db import AdminUser
        from apps.models.supplier_db import Supplier
        from apps.models.wallet_db import SupplierWallet, WalletTransaction
        from apps.models.statement_db import SupplierStatement
        from apps.models.settlements_db import AdminSettlement
        
        # 🛡️ مرحلة التزامن والتصحيح الذاتي للهيكل
        try:
            db.create_all() 
            
            # آلية إضافة الأعمدة المشفرة يدوياً إذا لم تكن موجودة (حل الـ UndefinedColumn)
            cols_to_add = [
                'sovereign_id_enc', 'trade_name_enc', 'owner_name_enc', 
                'id_type_enc', 'supply_category_enc', 'owner_phone_enc',
                'shop_phone_enc', 'province_enc', 'district_enc',
                'address_detail_enc', 'financial_company_enc', 'bank_name_enc', 'bank_acc_enc'
            ]
            for col in cols_to_add:
                db.session.execute(text(f'ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS {col} VARCHAR(255);'))
            db.session.commit()
            print("✅ [Database]: Schema synchronized and repaired successfully.")
            
        except Exception as e:
            print(f"❌ [Security DB Error]: {e}")

        # 🛡️ إدارة المستخدم
        @login_manager.user_loader
        def load_user(user_id):
            return AdminUser.query.get(int(user_id))

        # 🛡️ تسجيل دفاعي صارم للمسارات
        blueprints_map = [
            ('apps.auth_portal.routes', 'auth_portal', ''),
            ('apps.add_supplier.routes', 'add_supplier_bp', '/suppliers'),
            ('apps.financial_ops.routes', 'financial_blueprint', '/financial_ops'),
            ('apps.statement.routes', 'statement_blueprint', '/statement'),
            ('apps.admin_dashboard.routes', 'admin_dashboard', '/admin'),
            ('api.webhook', 'webhook_bp', '/api')
        ]

        for module_path, bp_name, prefix in blueprints_map:
            try:
                module = __import__(module_path, fromlist=[bp_name])
                blueprint = getattr(module, bp_name)
                app.register_blueprint(blueprint, url_prefix=prefix)
            except Exception as e:
                print(f"⚠️ Security Alert: Failed to register {bp_name} - Error: {e}")

        @app.route('/robots.txt')
        def robots_txt():
            return "User-agent: *\nDisallow: /", 200, {'Content-Type': 'text/plain'}

        @app.route('/')
        def root_redirect():
            return redirect('/login')

        # 🛡️ الحماية المتقدمة (Security Headers)
        @app.after_request
        def add_security_headers(response):
            response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com https://cdn.jsdelivr.net; "
                "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
                "img-src 'self' https://cdn.qumra.cloud; "
                "frame-ancestors 'none';"
            )
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-Robots-Tag"] = "noindex, nofollow, noarchive, nosnippet, noimageindex"
            response.headers["Referrer-Policy"] = "no-referrer"
            response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=(), payment=()"
            response.headers.pop("Server", None)
            return response

    return app

app = create_app()
