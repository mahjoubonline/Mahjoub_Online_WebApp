# coding: utf-8
# 📂 apps/__init__.py

import os
import importlib
from flask import Flask, session
from flask_wtf.csrf import CSRFProtect, generate_csrf # [تعديل 1]: استيراد الحماية
from apps.extensions import db, login_manager, migrate
from apps.models import AdminUser, Supplier, SupplierProfile
from apps.models.supplier_staff_db import SupplierStaff
from apps.models.wallet_db import SupplierWallet
from apps.utils.time_utils import format_full_timestamp

# [تعديل 2]: تهيئة كائن الحماية
csrf = CSRFProtect()

@login_manager.user_loader
def load_user(user_id):
    user_type = session.get('user_type')
    if user_type == 'admin': return AdminUser.query.get(int(user_id))
    elif user_type == 'supplier': return Supplier.query.get(int(user_id))
    elif user_type == 'staff': return SupplierStaff.query.get(int(user_id))
    return AdminUser.query.get(int(user_id)) or Supplier.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.jinja_env.filters['full_time'] = format_full_timestamp

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app) # [تعديل 3]: ربط الحماية بالتطبيق
    login_manager.login_view = 'suppliers_auth.login'

    # [تعديل 4]: إتاحة csrf_token في جميع القوالب
    @app.context_processor
    def inject_csrf_token():
        return dict(csrf_token=generate_csrf)

    with app.app_context():
        # إنشاء الجداول
        db.create_all()

        # --- سكريبت زرع البيانات (كما هو في كودك الأصلي) ---
        try:
            admin = AdminUser.query.filter_by(username='علي محجوب').first()
            if not admin:
                admin = AdminUser(username='علي محجوب')
                admin.set_password('123')
                db.session.add(admin)
                db.session.commit()
        except Exception as e:
            db.session.rollback()

        # ... (بقية سكريبتات الزرع الخاصة بك تظل كما هي) ...

        # 3. الاكتشاف التلقائي للموديولات
        apps_dir = app.root_path
        for item in os.listdir(apps_dir):
            item_path = os.path.join(apps_dir, item)
            if item in ['__pycache__', 'models', 'extensions', 'static', 'templates', 'migrations', 'utils', 'suppliers_auth']: continue
            registry_file = os.path.join(item_path, 'registry.py')
            if os.path.isdir(item_path) and os.path.exists(registry_file):
                try:
                    module = importlib.import_module(f"apps.{item}.registry")
                    if hasattr(module, 'register_module'): 
                        module.register_module(app)
                except Exception as e: 
                    print(f"⚠️ [Auto-Discovery] فشل تسجيل {item}: {e}")

    return app
