# coding: utf-8
# 📂 apps/__init__.py

import os
import importlib
from flask import Flask, redirect
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from sqlalchemy import inspect, text
import config

from apps.extensions import db, login_manager, migrate
from apps.api.qomrah_webhook import qomrah_bp

# تهيئة الأدوات (بدون تغيير)
csrf = CSRFProtect()
talisman = Talisman()
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"], storage_uri="memory://")

ADMIN_MODULES = {}
SUPPLIER_MODULES = {}

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    config.Config.validate_config()
    CORS(app, resources={r"/admin/*": {"origins": ["https://studio.apollographql.com", "http://localhost:5000"]}}, supports_credentials=True)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    
    # ... (باقي إعدادات talisman و Blueprints كما هي في ملفك)
    login_manager.login_view = 'suppliers_auth.login'
    app.register_blueprint(qomrah_bp)
    csrf.exempt(qomrah_bp)

    # 6. إعداد البيئة (التشخيص الذكي)
    with app.app_context():
        try:
            # اختبار الاتصال الأساسي
            db.session.execute(text("SELECT 1"))
            
            # فحص الجداول باستخدام Inspector
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"🔍 [Setup]: الجداول المكتشفة في قاعدة البيانات: {tables}")
            
            # إذا كانت قاعدة البيانات فارغة تماماً، نقوم بالبناء لمرة واحدة
            if not tables:
                print("⚡ [Setup]: قاعدة البيانات فارغة، جاري إنشاء الجداول...")
                db.create_all()
            
            # إضافة المالك (فقط إذا كان الجدول موجوداً)
            if 'admin_users' in tables:
                from apps.models.admin_db import AdminUser
                if not AdminUser.query.filter_by(username='علي محجوب').first():
                    owner = AdminUser(username='علي محجوب', role='Owner')
                    owner.set_password('123')
                    db.session.add(owner)
                    db.session.commit()
                    print("✅ [Setup]: تم إنشاء المستخدم المالك.")
            
        except Exception as e:
            print(f"❌ [Setup]: خطأ حرج في تهيئة قاعدة البيانات: {e}")
            db.session.rollback()

    return app
