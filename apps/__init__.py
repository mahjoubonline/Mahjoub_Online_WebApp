# coding: utf-8
from flask import Flask
from apps.extensions import db, login_manager
from config import Config

def create_app():
    """
    دالة المصنع (Application Factory) لإنشاء تطبيق Flask.
    """
    # 1. إنشاء التطبيق
    app = Flask(__name__)
    app.config.from_object(Config)

    # 2. تهيئة الإضافات
    db.init_app(app)
    login_manager.init_app(app)
    
    # تحديد مسار صفحة الدخول التلقائي
    login_manager.login_view = 'auth_portal.login' 

    # 3. دالة تعريف المستخدم (تحميل آمن للمستخدم)
    @login_manager.user_loader
    def load_user(user_id):
        from apps.models.admin_db import AdminUser
        return AdminUser.query.get(int(user_id))

    # 4. تسجيل الـ Blueprints (النوافذ المستقلة)
    # ملاحظة: يتم الاستيراد هنا لتجنب مشاكل الاستيراد الدائري (Circular Imports)
    
    # البوابة الرئيسية
    from apps.auth_portal import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    # لوحة التحكم
    from apps.admin_dashboard import admin_dashboard_bp
    app.register_blueprint(admin_dashboard_bp, url_prefix='/admin')
    
    # إدارة الموردين
    from apps.add_supplier import admin_suppliers_bp
    app.register_blueprint(admin_suppliers_bp, url_prefix='/suppliers')
    
    # إدارة المحفظة: تأكد أن الاسم في wallet/__init__.py هو 'wallet'
    from apps.wallet import wallet_bp
    app.register_blueprint(wallet_bp, url_prefix='/wallet')

    return app
