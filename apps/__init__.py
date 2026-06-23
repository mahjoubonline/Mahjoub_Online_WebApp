# coding: utf-8
# 📂 apps/__init__.py - المصنع السيادي للإدارة (نسخة معزولة تماماً ومصححة)

import os
import importlib
from flask import Flask, redirect, url_for
from flask_talisman import Talisman
from config import Config
from apps.extensions import db, login_manager, migrate

def create_app():
    # 1. إعداد المصنع
    app = Flask(__name__, 
                template_folder='templates', 
                static_folder='static', 
                static_url_path='/static',
                instance_relative_config=True)
    
    app.config.from_object(Config)

    # تحسينات الأمان
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        REMEMBER_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True
    )

    # 2. 🛡️ سياسة أمان المحتوى (CSP)
    Talisman(app, force_https=True, content_security_policy={
        'default-src': ["'self'"],
        'style-src': ["'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com", "https://fonts.googleapis.com", "https://cdn.jsdelivr.net"],
        'script-src': ["'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com", "https://cdn.jsdelivr.net"],
        'font-src': ["'self'", "data:", "https://fonts.gstatic.com", "https://cdnjs.cloudflare.com", "https://cdn.jsdelivr.net"],
        'img-src': ["'self'", "data:", "https://*"]
    }, frame_options='SAMEORIGIN', referrer_policy='strict-origin-when-cross-origin')

    # 3. تهيئة الإضافات
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_portal.login'

    @login_manager.user_loader
    def load_user(user_id):
        from apps.models.admin_db import AdminUser
        return AdminUser.query.get(int(user_id))

    # 4. تسجيل مسارات الإدارة فقط
    core_blueprints = [
        ('apps.auth_portal.routes', 'auth_portal', '/auth'),
        ('apps.admin_dashboard.routes', 'admin_dashboard', '/admin'),
        ('apps.wallet.routes', 'wallet_app', '/wallet'),
        ('apps.vault.routes', 'vault_bp', '/vault'),
        ('apps.orders.routes', 'orders_bp', '/orders'),
        ('apps.api.webhooks', 'webhooks_bp', '/api')
    ]

    for module_path, bp_name, prefix in core_blueprints:
        try:
            module = importlib.import_module(module_path)
            app.register_blueprint(getattr(module, bp_name), url_prefix=prefix)
        except Exception as e:
            print(f"🚨 [System] خطأ في تحميل مسار الإدارة {bp_name}: {e}")

    # 5. عزل تام للموردين عبر الـ Registry الديناميكي
    apps_dir = os.path.dirname(__file__)
    for folder in os.listdir(apps_dir):
        if folder in {'suppliers_auth_portal', 'suppliers_dashboard'}:
            registry_path = os.path.join(apps_dir, folder, 'registry.py')
            if os.path.exists(registry_path):
                try:
                    module = importlib.import_module(f'apps.{folder}.registry')
                    if hasattr(module, 'register_app'):
                        module.register_app(app)
                except Exception as e:
                    print(f"⚠️ [Isolation] الموردون {folder} فشلوا في التسجيل، لكن الإدارة تعمل: {e}")

    @app.route('/')
    def index():
        return redirect(url_for('auth_portal.login'))

    # 6. إعداد البيانات
    with app.app_context():
        try:
            from apps.models.admin_db import AdminUser
            db.create_all()
            
            owner_username = 'علي محجوب'
            if not AdminUser.query.filter_by(username=owner_username).first():
                admin = AdminUser(username=owner_username, role='Owner', phone_number='779077746')
                admin.set_password('123')
                db.session.add(admin)
                db.session.commit()
        except Exception as e:
            print(f"⚠️ [Error] خطأ في قاعدة البيانات: {e}")

    return app
