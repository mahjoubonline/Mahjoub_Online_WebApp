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

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # تهيئة الإضافات
    db.init_app(app)
    migrate.init_app(app, db)
    
    # ... (باقي تهيئة الإضافات مثل login_manager, csrf, etc. كما هي)

    with app.app_context():
        # 1. اختبار الاتصال بقاعدة البيانات
        try:
            db.engine.connect().execute(text("SELECT 1"))
            print("✅ [Setup]: الاتصال بقاعدة البيانات نجح.")
        except Exception as e:
            print(f"❌ [Setup]: فشل الاتصال بقاعدة البيانات: {e}")
            return app

        # 2. استيراد الموديلات (لضمان تسجيلها في Metadata)
        from apps.models import (
            Supplier, AdminUser, Marketer, ExchangeRate, AdminStaff, 
            SupplierProfile, SupplierStaff, SupplierWallet, WalletTransaction,
            OrderFinancial, Order, OrderItem, SyncLog
        )

        # 3. بناء الجداول بشكل قسري
        try:
            db.metadata.create_all(bind=db.engine)
            print("✅ [Setup]: تم بناء الجداول بنجاح.")
        except Exception as e:
            print(f"❌ [Setup]: خطأ أثناء بناء الجداول: {e}")

        # 4. محاولة إنشاء المالك (بأمان)
        try:
            if not AdminUser.query.filter_by(username='علي محجوب').first():
                owner = AdminUser(username='علي محجوب', role='Owner')
                owner.set_password('123')
                db.session.add(owner)
                db.session.commit()
                print("✅ [Setup]: تم إنشاء المستخدم المالك.")
        except Exception as e:
            db.session.rollback()
            print(f"ℹ️ [Setup]: تخطي إضافة المالك (قد يكون الجدول غير جاهز): {e}")

    return app
