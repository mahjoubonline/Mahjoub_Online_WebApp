# 📂 apps/__init__.py

import os
import importlib
from flask import Flask
from apps.extensions import db, login_manager, migrate
# حذفنا استيراد الموديلات من هنا تماماً لمنع التضارب

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # تهيئة الإضافات
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    with app.app_context():
        # --- نظام الاكتشاف التلقائي (Auto-Discovery) ---
        apps_dir = app.root_path
        
        # البحث في جميع المجلدات داخل apps
        for item in os.listdir(apps_dir):
            item_path = os.path.join(apps_dir, item)
            
            # استثناء المجلدات غير الموديولية (مثل __pycache__ أو models)
            if item in ['__pycache__', 'models', 'extensions', 'static', 'templates']:
                continue

            registry_file = os.path.join(item_path, 'registry.py')
            
            if os.path.isdir(item_path) and os.path.exists(registry_file):
                try:
                    module_path = f"apps.{item}.registry"
                    module = importlib.import_module(module_path)
                    
                    if hasattr(module, 'register_module'):
                        module.register_module(app)
                        print(f"✅ [Auto-Discovery] تم تسجيل الموديول: {item}")
                except Exception as e:
                    print(f"⚠️ [Auto-Discovery] فشل تسجيل {item}: {e}")

        # تثبيت الـ Mappers بعد التسجيل الكامل
        db.configure_mappers()

    return app
