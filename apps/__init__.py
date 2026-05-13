from flask import Flask
import os
from models.supplier_db import db

def create_app():
    app = Flask(__name__)
    
    # الإعدادات السيادية
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'mahjoub_online_2026_key'
    
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///mahjoub_admin.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # تسجيل المحركات (Blueprints)
    from .admin_dashboard.routes import admin_dashboard
    from .add_supplier.routes import admin_suppliers
    
    # لوحة التحكم المركزية
    app.register_blueprint(admin_dashboard, url_prefix='/admin')
    # نظام إضافة الموردين
    app.register_blueprint(admin_suppliers, url_prefix='/admin/suppliers')

    with app.app_context():
        db.create_all()

    return app
