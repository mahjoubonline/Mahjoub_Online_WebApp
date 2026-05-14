# coding: utf-8
# 🌟 استيراد المكتبات الأساسية لتشغيل المحرك
import os
from flask import Flask
from models.admin_db import db, AdminUser # 💡 تأكد أن الكلاس في admin_db.py اسمه AdminUser

def create_app():
    """
    دالة بناء التطبيق: تقوم بتجهيز الإعدادات والروابط.
    """
    app = Flask(__name__)
    
    # 🔑 إعداد مفتاح الأمان (ضروري لعمل Flask-WTF الذي أضفته في المتطلبات)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'MAHJOUB_SECRET_2026')
    
    # 🗄️ ربط قاعدة البيانات (PostgreSQL) بناءً على requirements.txt
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # تهيئة قاعدة البيانات مع التطبيق
    db.init_app(app)

    with app.app_context():
        # إنشاء الجداول إذا لم تكن موجودة
        db.create_all()

    return app

# 🚀 هذا هو السطر الأهم ليعمل الـ Procfile:
# gunicorn سيقوم بالبحث عن متغير اسمه 'app' داخل ملف 'run'
app = create_app()

if __name__ == "__main__":
    # التشغيل المحلي للتطوير
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
