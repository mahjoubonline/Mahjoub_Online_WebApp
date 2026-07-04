# coding: utf-8
# 📂 apps/__init__.py

import os
import importlib
from flask import Flask
from flask_wtf.csrf import CSRFProtect, generate_csrf
from apps.extensions import db, login_manager, migrate
from apps.utils.time_utils import format_full_timestamp

csrf = CSRFProtect()

# هذا القاموس هو المحرك الذي يغذي الشريط الجانبي
REGISTERED_MODULES = {}

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # 1. تسجيل الموديولات الأساسية
    from apps.auth_portal.routes import auth_portal
    from apps.admin_dashboard.routes import admin_dashboard
    
    app.register_blueprint(auth_portal, url_prefix='/auth')
    app.register_blueprint(admin_dashboard, url_prefix='/admin')
    
    # إضافة الفلاتر
    app.jinja_env.filters['full_time'] = format_full_timestamp

    # إعداد الإضافات
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    @app.context_processor
    def inject_vars():
        return dict(
            csrf_token=generate_csrf,
            registered_modules=REGISTERED_MODULES
        )

    # 2. نظام التسجيل التلقائي الذكي (خارج app_context لضمان توفره عند بدء التشغيل)
    apps_dir = app.root_path
    ignored_dirs = ['__pycache__', 'models', 'extensions', 'static', 'templates', 'migrations', 'utils', 'suppliers_auth', 'auth_portal', 'admin_dashboard']
    
    for item in os.listdir(apps_dir):
        item_path = os.path.join(apps_dir, item)
        if os.path.isdir(item_path) and item not in ignored_dirs:
            registry_file = os.path.join(item_path, 'registry.py')
            if os.path.exists(registry_file):
                try:
                    module = importlib.import_module(f"apps.{item}.registry")
                    if hasattr(module, 'register_module'):
                        module.register_module(app)
                        REGISTERED_MODULES[item] = {
                            "display_name": getattr(module, 'MODULE_NAME', item.capitalize()),
                            "icon": getattr(module, 'MODULE_ICON', 'fa-folder'),
                            "links": getattr(module, 'LINKS', {}),
                            "active": True
                        }
                except Exception as e:
                    print(f"⚠️ [Auto-Discovery] Error in {item}: {e}")

    # 3. تحديث خريطة المسارات بعد تسجيل كل شيء
    with app.app_context():
        db.create_all()
        # زرع المستخدم الافتراضي
        try:
            from apps.models.admin_db import AdminUser
            admin = AdminUser.query.filter_by(username='علي محجوب').first()
            if not admin:
                admin = AdminUser(username='علي محجوب')
                admin.set_password('123')
                db.session.add(admin)
                db.session.commit()
        except Exception:
            db.session.rollback()

    app.config['ENDPOINT_MAP'] = {rule.endpoint for rule in app.url_map.iter_rules()}
    
    return app
