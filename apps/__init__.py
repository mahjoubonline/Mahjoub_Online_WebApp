# coding: utf-8
# 📂 apps/__init__.py - المصنع السيادي الموحد (نسخة الفحص الاستباقي للـ 404)

import os
import importlib
from flask import Flask, redirect
from flask_talisman import Talisman
from config import Config
from apps.extensions import db, login_manager, migrate

def create_app():
    app = Flask(__name__, 
                template_folder='templates', 
                static_folder='static', 
                static_url_path='/static',
                instance_relative_config=True)
    
    app.config.from_object(Config)

    # 1. إعدادات الأمان
    app.config.update(SESSION_COOKIE_SECURE=True, REMEMBER_COOKIE_SECURE=True, SESSION_COOKIE_HTTPONLY=True)
    Talisman(app, force_https=True, content_security_policy={'default-src': ["'self'"]}, frame_options='SAMEORIGIN')

    # 2. الإضافات
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # 3. تسجيل المسارات الأساسية
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
            print(f"🚨 [System] خطأ في تسجيل {bp_name}: {e}")

    # 4. الاكتشاف التلقائي
    apps_dir = os.path.dirname(__file__)
    ignore = {'models', 'extensions', 'static', 'templates', '__pycache__', 'api', 'auth_portal', 'admin_dashboard', 'wallet', 'vault', 'orders'}
    
    for folder in os.listdir(apps_dir):
        if folder in ignore or not os.path.isdir(os.path.join(apps_dir, folder)): continue
        reg_path = os.path.join(apps_dir, folder, 'registry.py')
        if os.path.exists(reg_path):
            try:
                mod = importlib.import_module(f'apps.{folder}.registry')
                if hasattr(mod, 'register_app'): mod.register_app(app)
            except Exception as e: print(f"⚠️ [Auto-Discovery] فشل {folder}: {e}")

    # 5. [DEBUG] طباعة المسارات الفعلية (هذا سيكشف سبب الـ 404 في الـ Logs)
    print("📋 [DEBUG] المسارات المسجلة:")
    for rule in app.url_map.iter_rules():
        print(f"DEBUG: Mapping {rule.endpoint} -> {rule.rule}")

    @app.route('/')
    def index():
        login_path = os.environ.get('ADMIN_LOGIN_PATH', '/m7jb_sovereign_hq_v2_99x')
        return redirect(f'/auth{login_path}')

    return app
