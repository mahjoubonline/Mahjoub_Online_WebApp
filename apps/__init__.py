# coding: utf-8
# 📂 apps/__init__.py

import os
import importlib
from flask import Flask, session, redirect, url_for
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_talisman import Talisman  # للحماية من XSS و Clickjacking
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from apps.extensions import db, login_manager, migrate
from apps.utils.time_utils import format_full_timestamp

csrf = CSRFProtect()
talisman = Talisman() # الحماية الأمنية
limiter = Limiter(key_func=get_remote_address) # الحماية من الريبوتات والزحف العنيف

ADMIN_MODULES = {}
SUPPLIER_MODULES = {}

@login_manager.user_loader
def load_user(user_id):
    try:
        from apps.models.admin_db import AdminUser
        from apps.models.supplier_db import Supplier
        from apps.models.supplier_staff_db import SupplierStaff
        user_type = session.get('user_type')
        uid = int(user_id)
        if user_type == 'admin': return AdminUser.query.get(uid)
        elif user_type == 'supplier': return Supplier.query.get(uid)
        elif user_type == 'staff': return SupplierStaff.query.get(uid)
        return None
    except Exception:
        return None

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # 1. تهيئة أدوات الحماية
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    
    # Talisman يضيف Headers أمنية قوية تلقائياً
    talisman.init_app(app, content_security_policy={
        'default-src': ["'self'"],
        'script-src': ["'self'", "https://code.jquery.com", "https://cdn.jsdelivr.net"],
        'style-src': ["'self'", "https://cdn.jsdelivr.net", "'unsafe-inline'"],
    })

    app.jinja_env.filters['full_time'] = format_full_timestamp
    login_manager.login_view = 'suppliers_auth.login'
    
    # تسجيل الموديولات (كما في كودك الأصلي)
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
                            mod_data = {
                                "display_name": getattr(module, 'MODULE_NAME', item.capitalize()),
                                "icon": getattr(module, 'MODULE_ICON', 'fa-folder'),
                                "links": getattr(module, 'LINKS', {}),
                            }
                            if getattr(module, 'SHOW_IN_SUPPLIER', False):
                                SUPPLIER_MODULES[item] = mod_data
                            else:
                                ADMIN_MODULES[item] = mod_data
                    except Exception as e:
                        print(f"❌ خطأ في تسجيل {item}: {e}")

    @app.route('/')
    def index():
        return redirect('/supplier/login')

    @app.context_processor
    def inject_vars():
        return dict(
            csrf_token=generate_csrf,
            registered_modules=ADMIN_MODULES,
            supplier_modules=SUPPLIER_MODULES
        )

    with app.app_context():
        db.create_all()
        # [زراعة المالك]
        from apps.models.admin_db import AdminUser
        if not AdminUser.query.filter_by(username='علي محجوب').first():
            owner = AdminUser(username='علي محجوب', role='Owner')
            owner.set_password('123')
            db.session.add(owner)
            db.session.commit()
    
    return app
