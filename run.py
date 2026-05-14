# coding: utf-8
# 🌟 ملف التشغيل لمنصة محجوب أونلاين - متوافق مع Python 3.12.3
import os
import sys

# التأكد من إضافة المسار الحالي لبيئة العمل لضمان رؤية المجلدات الفرعية
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask

# 🛡️ محاولة استيراد آمنة لفك "تجميد" التطبيق
try:
    # الاستيراد من مجلد models (تأكد من وجود ملف __init__.py هناك)
    from models.admin_db import db, AdminUser
    print("✅ تم استيراد النماذج بنجاح")
except ImportError as e:
    print(f"❌ فشل الاستيراد: {e}")
    # تعريف كائنات وهمية مؤقتاً لمنع انهيار gunicorn أثناء التشخيص
    db = None
    AdminUser = None

def create_app():
    app = Flask(__name__)
    
    # إعدادات قاعدة البيانات المربوطة بـ Railway
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_key_2026')

    if db:
        db.init_app(app)
        with app.app_context():
            # إنشاء الجداول إذا كانت مفقودة
            try:
                db.create_all()
            except Exception as e:
                print(f"⚠️ خطأ في إنشاء الجداول: {e}")

    @app.route('/')
    def status():
        return "Mahjoub Online: System is Operational"

    return app

# 🚀 هذا المتغير هو ما يبحث عنه Procfile (web: gunicorn run:app)
app = create_app()

if __name__ == "__main__":
    app.run()
