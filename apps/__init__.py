# coding: utf-8
# 📂 apps/__init__.py

import os
import importlib
from flask import Flask, session
from flask_wtf.csrf import CSRFProtect, generate_csrf
from apps.extensions import db, login_manager, migrate
from apps.utils.time_utils import format_full_timestamp

csrf = CSRFProtect()
ADMIN_MODULES = {}
SUPPLIER_MODULES = {}

@login_manager.user_loader
def load_user(user_id):
    try:
        from apps.models import AdminUser, Supplier, SupplierStaff
        user_type = session.get('user_type')
        uid = int(user_id)
        if user_type == 'admin': return AdminUser.query.get(uid)
        elif user_type == 'supplier': return Supplier.query.get(uid)
        elif user_type == 'staff': return SupplierStaff.query.get(uid)
        return AdminUser.query.get(uid) or Supplier.query.get(uid) or SupplierStaff.query.get(uid)
    except Exception as e:
        return None

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # 1. تهيئة الإضافات
    app.jinja_env.filters['full_time'] = format_full_timestamp
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # تم إزالة التسجيل اليدوي لـ suppliers_auth_portal ليعمل Auto-Discovery
    login_manager.login_view = 'suppliers_auth.login' # تصحيح الـ endpoint الصحيح
    
    # 2. اكتشاف الموديولات (تم إزالة suppliers_auth_portal من ignored_dirs)
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
                            
                            # العزل وتجهيز القوائم
                            mod_data = {
                                "display_name": getattr(module, 'MODULE_NAME', item.capitalize()),
                                "icon": getattr(module, 'MODULE_ICON', 'fa-folder'),
                                "links": getattr(module, 'LINKS', {}),
                            }
                            
                            # نستخدم القيم الموجودة في registry.py
                            if getattr(module, 'SHOW_IN_SUPPLIER', False):
                                SUPPLIER_MODULES[item] = mod_data
                            else:
                                ADMIN_MODULES[item] = mod_data
                                
                            print(f"✅ تم تسجيل الموديول: {item}")
                    except Exception as e:
                        print(f"❌ خطأ في تسجيل {item}: {e}")

    # 3. حقن المتغيرات
    @app.context_processor
    def inject_vars():
        return dict(
            csrf_token=generate_csrf,
            registered_modules=ADMIN_MODULES,
            supplier_modules=SUPPLIER_MODULES
        )

    # 4. تهيئة قاعدة البيانات
    with app.app_context():
        db.create_all()
        # (باقي كود تهيئة المسؤول كما هو...)
    
    return app
