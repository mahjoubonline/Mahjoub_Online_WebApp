from flask import Flask
import os
from models.supplier_db import db  # استيراد قاعدة البيانات الموحدة

def create_app():
    app = Flask(__name__)
    
    # --- الإعدادات السيادية للربط مع Railway ---
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'mahjoub_online_2026_key'
    
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///mahjoub_admin.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # تهيئة قاعدة البيانات مع التطبيق
    db.init_app(app)

    # --- تسجيل المحركات (Blueprints) بمسارات نظيفة ومنفصلة ---

    # 1. بوابة التحقق (Authentication)
    from .auth_portal.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # 2. لوحة التحكم المركزية (Admin Dashboard)
    # ملاحظة: هذا المحرك يدير الواجهة الرئيسية للإحصائيات وسجل الموردين
    from .admin_dashboard.routes import admin_dashboard
    app.register_blueprint(admin_dashboard, url_prefix='/admin')

    # 3. محرك إدارة الموردين (Add Supplier)
    # تم ربطه هنا ليعمل تحت مسار فرعي لضمان التنظيم
    from .add_supplier.routes import admin_suppliers
    app.register_blueprint(admin_suppliers, url_prefix='/admin/suppliers')

    # إنشاء الجداول تلقائياً في حالة عدم وجودها (اختياري للبيئة التطويرية)
    with app.app_context():
        db.create_all()

    return app
