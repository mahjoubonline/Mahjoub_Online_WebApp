# coding: utf-8
# 📂 apps/__init__.py

import os
import importlib
from flask import Flask, session
from apps.extensions import db, login_manager, migrate
from apps.models.admin_db import AdminUser
from apps.models import Supplier
from apps.models.supplier_staff_db import SupplierStaff
from apps.models.supplier_profile_db import SupplierProfile

# دالة لتحميل المستخدم (تعتمد الآن على نوع المستخدم في الجلسة)
@login_manager.user_loader
def load_user(user_id):
    user_type = session.get('user_type')
    
    if user_type == 'admin':
        return AdminUser.query.get(int(user_id))
    elif user_type == 'supplier':
        return Supplier.query.get(int(user_id))
    elif user_type == 'staff':
        return SupplierStaff.query.get(int(user_id))
    
    return AdminUser.query.get(int(user_id)) or Supplier.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # تهيئة الإضافات
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    login_manager.login_view = 'suppliers_auth.login' 

    with app.app_context():
        # 1. بناء الجداول
        try:
            db.create_all()
            print("✅ [Database]: تم فحص وبناء الجداول بنجاح.")
        except Exception as e:
            print(f"⚠️ [Database]: خطأ أثناء محاولة بناء الجداول: {e}")

        # 2. إنشاء المستخدمين الافتراضيين (المالك والموظف)
        try:
            # إنشاء الإداري
            if not AdminUser.query.filter_by(username='علي محجوب').first():
                admin = AdminUser(username='علي محجوب', role='Owner')
                admin.set_password('123')
                db.session.add(admin)
            
            # إنشاء المورد (المالك)
            supplier = Supplier.query.filter_by(username='وائل محجوب').first()
            if not supplier:
                supplier = Supplier(
                    username='وائل محجوب', 
                    trade_name='محجوب أونلاين',
                    phone='0000000000'
                )
                supplier.set_password('123')
                db.session.add(supplier)
                db.session.flush() # تثبيت مؤقت للحصول على ID
                
                # إنشاء البروفايل تلقائياً للمورد
                profile = SupplierProfile(supplier_id=supplier.id, trade_name='محجوب أونلاين')
                db.session.add(profile)

            # إنشاء موظف افتراضي تابع للمورد
            if not SupplierStaff.query.filter_by(username='موظف_1').first():
                staff = SupplierStaff(
                    supplier_id=supplier.id,
                    username='موظف_1',
                    email='staff1@mahjoub.com',
                    role='worker'
                )
                staff.set_password('123')
                db.session.add(staff)
            
            db.session.commit()
            print("✅ [Users]: تم زرع المالك والموظف والبروفايل بنجاح.")
        except Exception as e:
            db.session.rollback()
            print(f"⚠️ [Users]: خطأ أثناء إنشاء المستخدمين: {e}")

        # 3. --- نظام الاكتشاف التلقائي (Auto-Discovery) ---
        apps_dir = app.root_path
        for item in os.listdir(apps_dir):
            item_path = os.path.join(apps_dir, item)
            
            if item in ['__pycache__', 'models', 'extensions', 'static', 'templates', 'migrations']:
                continue

            registry_file = os.path.join(item_path, 'registry.py')
            
            if os.path.isdir(item_path) and os.path.exists(registry_file):
                try:
                    module = importlib.import_module(f"apps.{item}.registry")
                    if hasattr(module, 'register_module'):
                        module.register_module(app)
                        print(f"✅ [Auto-Discovery] تم تسجيل الموديول: {item}")
                except Exception as e:
                    print(f"⚠️ [Auto-Discovery] فشل تسجيل {item}: {e}")

        db.configure_mappers()

    return app
