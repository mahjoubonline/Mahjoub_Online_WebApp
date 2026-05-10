# core/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# 1. تهيئة قاعدة البيانات السيادية (SQLAlchemy)
db = SQLAlchemy()

# 2. تهيئة مدير الجلسات والحماية (Login Manager)
login_manager = LoginManager()

# إعدادات الحماية الافتراضية
login_manager.login_view = 'admin.login' # توجيه المستخدم لصفحة الدخول إذا لم يكن مسجلاً
login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى مركز القيادة."
login_manager.login_message_category = "info"

"""
ملاحظة تقنية للمؤسس علي:
هذا الملف يجب أن يتم استيراد 'db' منه في كل مكان (Models, Routes, Logic)
بينما يتم استدعاء 'db.init_app(app)' مرة واحدة فقط في ملف التشغيل الرئيسي (app.py).
"""
