from flask import Flask
import os
from models.supplier_db import db  # استيراد قاعدة البيانات الموحدة

def create_app():
    # إنشاء التطبيق
    app = Flask(__name__)
    
    # --- الإعدادات السيادية ---
    # جلب مفتاح الأمان من البيئة أو استخدام المفتاح الافتراضي
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'mahjoub_online_2026_key'
    
    # إعداد قاعدة البيانات لتتوافق مع بيئة Railway أو المحلي
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///mahjoub_admin.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ربط قاعدة البيانات بالتطبيق
    db.init_app(app)

    # 🛡️ تسجيل المحركات (Blueprints) لضمان تدفق البيانات:

    # 1. محرك بوابة التحقق (Auth Portal)
    from .auth_portal.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # 2. محرك لوحة التحكم (Admin Dashboard)
    from .admin_dashboard.routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # 3. محرك إدارة الموردين (Add Supplier)
    # ملاحظة: تم دمج هذا المحرك تحت مسار فرعي لضمان عدم التضارب مع لوحة التحكم
    from .add_supplier.routes import admin_suppliers
    app.register_blueprint(admin_suppliers, url_prefix='/admin/suppliers')

    return app
