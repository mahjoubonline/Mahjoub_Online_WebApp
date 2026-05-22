# apps/__init__.py

from flask import Flask
from apps.extensions import db, login_manager # استيراد من ملف extensions
from config import Config

# تأكد من استيراد موديل المسؤول (AdminUser)
from apps.models.admin_db import AdminUser 

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # تهيئة الإضافات
    db.init_app(app)
    login_manager.init_app(app)

    # --- هذا الجزء هو المفقود والسبب في انهيار الموقع ---
    @login_manager.user_loader
    def load_user(user_id):
        # هنا نعيد كائن المستخدم من قاعدة البيانات بناءً على الـ ID
        return AdminUser.query.get(int(user_id))
    # -----------------------------------------------------

    # تسجيل الـ Blueprints (باقي كود تسجيل المسارات الخاص بك)
    # ...
    
    return app
