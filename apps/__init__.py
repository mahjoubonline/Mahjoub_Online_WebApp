from flask import Flask
from models.supplier_db import db  # استيراد قاعدة البيانات لربطها بالتطبيق

def create_app():
    # إنشاء التطبيق
    app = Flask(__name__)
    
    # إعدادات الحماية والتشفير السيادية
    app.config['SECRET_KEY'] = 'mahjoub_online_2026_key'
    # إعداد قاعدة البيانات (تأكد من تعديل الرابط حسب إعدادات Railway لديك)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/mahjoub_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ربط قاعدة البيانات بالتطبيق
    db.init_app(app)

    # 🛡️ تسجيل المحركات (Blueprints) بالأسماء الصحيحة والمثبتة:

    # 1. محرك بوابة التحقق (Authentication)
    from .auth_portal.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # 2. محرك لوحة التحكم الإدارية (Admin Dashboard)
    # ملاحظة: الاسم البرمجي داخل الملف هو 'admin_bp'
    from .admin_dashboard.routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # 3. محرك إدارة الموردين (Add Supplier)
    # ملاحظة: الاسم البرمجي داخل الملف هو 'admin_suppliers' كما ثبتناه سابقاً
    from .add_supplier.routes import admin_suppliers
    app.register_blueprint(admin_suppliers, url_prefix='/admin')

    return app
