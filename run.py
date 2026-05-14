# coding: utf-8
# 🌟 ملف التشغيل الرئيسي لمنصة محجوب أونلاين
import os
import sys

# التأكد من أن المجلد الحالي مضاف لمسار النظام لضمان صحة الاستيراد
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask

# 🛡️ محاولة استيراد قاعدة البيانات بحذر لتجنب الانهيار المفاجئ
try:
    from models.admin_db import db, AdminUser
    print("✅ تم استيراد نماذج قاعدة البيانات بنجاح")
except ImportError as e:
    print(f"❌ خطأ في الاستيراد: {e}")
    # تعريف كائن وهمي لمنع الانهيار الكامل أثناء الفحص
    db = None 

def create_app():
    app = Flask(__name__)
    
    # إعدادات الأمان (مهمة لـ Flask-WTF في requirements.txt)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-key-for-dev')
    
    # ربط قاعدة البيانات (PostgreSQL) الظاهرة في image_77d5fa.png
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if db:
        db.init_app(app)
        with app.app_context():
            try:
                db.create_all()
            except Exception as e:
                print(f"⚠️ فشل إنشاء الجداول: {e}")

    @app.route('/')
    def health_check():
        return "Mahjoub Online is Running!"

    return app

# الكائن الذي يبحث عنه الـ Procfile عبر الأمر run:app
app = create_app()

if __name__ == "__main__":
    app.run()
