# coding: utf-8
# 🛠️ ملف الامتدادات المركزي - منصة محجوب أونلاين 2026
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# تهيئة الامتدادات (بدون ربطها بالتطبيق حالياً - يتم ذلك في create_app)
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

# هذا الملف الآن هو المصدر الموثوق الوحيد لـ db و login_manager
