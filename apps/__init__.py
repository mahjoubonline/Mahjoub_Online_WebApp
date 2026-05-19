# coding: utf-8
# 🏢 المصنع المركزي للنواة - منصة محجوب أونلاين 2026

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

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
            db.session.commit()
        except Exception as e:
            app.logger.error(f"❌ خطأ في تهيئة الجداول: {str(e)}")
        finally:
            db.session.close()

    login_manager.login_view = 'auth_portal.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        from apps.models.admin_db import AdminUser
        return AdminUser.query.get(int(user_id))

    # 📥 الاستيرادات
    from apps.auth_portal import auth_blueprint
    from apps.admin_dashboard.routes import admin_dashboard
    from apps.add_supplier.routes import admin_suppliers_bp
    from apps.wallet.routes import admin_wallet

    # ⚙️ تسجيل البلوبرينتس
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(admin_dashboard, url_prefix='/admin')
    
    # تسجيل الموردين والمحافظ (بما أن البلوبرينت في routes.py هو 'add_supplier')
    app.register_blueprint(admin_suppliers_bp, url_prefix='/admin')
    app.register_blueprint(admin_wallet, url_prefix='/admin')

    return app
