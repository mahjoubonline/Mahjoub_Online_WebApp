# coding: utf-8
# 🏢 المصنع المركزي للنواة - منصة محجوب أونلاين 2026

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# إنشاء الكائنات المركزية كنسخ مستقلة لمنع التعارض الدائري
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config)

    app.json.ensure_ascii = False
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        import apps.models.admin_db
        import apps.models.supplier_db
        import apps.models.wallet_db
        
        try:
            db.create_all()
            # (تم اختصار كود صيانة قاعدة البيانات هنا للاختصار، هو كما هو في ملفك الأصلي)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"❌ تعذر توليد الجداول: {str(e)}")
        finally:
            db.session.close()

    login_manager.login_view = 'auth_portal.login'
    login_manager.login_message = 'يرجى إثبات الهوية الرقمية للوصول إلى المنطقة السيادية.'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        from apps.models.admin_db import AdminUser
        return AdminUser.query.get(int(user_id))

    # 📥 الاستيراد السيادي الموحد للبلوبرينتس
    from apps.auth_portal import auth_blueprint
    # التعديل هنا: استخدام الاسم الذي يتطابق مع ملف routes.py الخاص بك
    from apps.admin_dashboard.routes import admin_dashboard 
    from apps.add_supplier.routes import admin_suppliers_bp
    from apps.wallet.routes import admin_wallet

    # ⚙️ تسجيل المسارات (تم توحيد الـ prefix لضمان عمل url_for)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    # 🎯 تم تسجيل البلوبرينت باسم 'admin_dashboard' ليتطابق مع ما هو موجود في admin_base.html
    app.register_blueprint(admin_dashboard, url_prefix='/admin')
    
    app.register_blueprint(admin_suppliers_bp, url_prefix='/admin')
    app.register_blueprint(admin_wallet, url_prefix='/admin')

    return app
