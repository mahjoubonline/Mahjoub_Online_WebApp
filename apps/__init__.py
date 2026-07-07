# coding: utf-8
# 📂 apps/__init__.py

import os
import importlib
from flask import Flask, session, redirect, url_for
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from apps.extensions import db, login_manager, migrate
from apps.utils.time_utils import format_full_timestamp

# تهيئة الأدوات
csrf = CSRFProtect()
talisman = Talisman()
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

ADMIN_MODULES = {}
SUPPLIER_MODULES = {}

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # تهيئة الإضافات
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    
    # Talisman - إعدادات الأمان
    talisman.init_app(app, 
        content_security_policy={
            'default-src': ["'self'"],
            'style-src': ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com", "https://cdn.jsdelivr.net"],
            'font-src': ["'self'", "https://fonts.gstatic.com", "https://cdn.jsdelivr.net"],
            'script-src': ["'self'", "'unsafe-inline'", "'unsafe-eval'", "https://code.jquery.com", "https://cdn.jsdelivr.net"],
            'img-src': ["'self'", "data:", "*"]
        },
        force_https=False 
    )

    app.jinja_env.filters['full_time'] = format_full_timestamp
    login_manager.login_view = 'suppliers_auth.login'
    
    # [تعديل] استثناء مسارات الـ API من الحماية الصارمة للـ CSRF
    from apps.api.qomrah_webhook import qomrah_bp
    app.register_blueprint(qomrah_bp)
    csrf.exempt(qomrah_bp) # استثناء الويب هوك من CSRF لأنه قادم من جهة خارجية (قمرة)

    # تسجيل الموديولات (الديناميكي)
    apps_dir = app.root_path 
    ignored_dirs = ['__pycache__', 'models', 'extensions', 'static', 'templates', 'migrations', 'utils', 'api']
    
    if os.path.exists(apps_dir):
        for item in os.listdir(apps_dir):
            item_path = os.path.join(apps_dir, item)
            if os.path.isdir(item_path) and item not in ignored_dirs:
                registry_file = os.path.join(item_path, 'registry.py')
                if os.path.exists(registry_file):
                    try:
                        module = importlib.import_module(f"apps.{item}.registry")
                        if hasattr(module, 'register_module'):
                            module.register_module(app)
                            # ... (بقية منطق تسجيل الموديلات)
                    except Exception as e:
                        print(f"❌ خطأ في تسجيل {item}: {e}")

    @app.route('/')
    def index():
        return redirect('/supplier/login')

    @app.context_processor
    def inject_vars():
        return dict(csrf_token=generate_csrf, registered_modules=ADMIN_MODULES, supplier_modules=SUPPLIER_MODULES)

    with app.app_context():
        db.create_all()
        from apps.models.admin_db import AdminUser
        if not AdminUser.query.filter_by(username='علي محجوب').first():
            owner = AdminUser(username='علي محجوب', role='Owner')
            owner.set_password('123')
            db.session.add(owner)
            db.session.commit()
    
    return app
