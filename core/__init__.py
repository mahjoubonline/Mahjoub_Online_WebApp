from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# تعريف الكائنات هنا لضمان إمكانية استيرادها في الملفات الأخرى دون أخطاء
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # تحميل الإعدادات
    app.config.from_object('config.Config')

    # تهيئة الإضافات
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        # استيراد الموديلات أولاً لبناء الجداول
        from core.models.user import User
        db.create_all()

        # استيراد وتسجيل البوابات (الاستيراد هنا يمنع خطأ 500)
        from admin_panel.routes import admin_bp
        from supplier_panel.routes import supplier_bp
        
        app.register_blueprint(admin_bp, url_prefix='/admin')
        app.register_blueprint(supplier_bp, url_prefix='/supplier')

    @app.route('/')
    def index():
        return redirect(url_for('admin_panel.admin_login'))

    return app

@login_manager.user_loader
def load_user(user_id):
    from core.models.user import User
    return db.session.get(User, int(user_id))
