import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def start_over():
    print("🧹 تنظيف قاعدة البيانات وبناء الهيكل الجديد...")
    
    # بناء المجلدات يدوياً في السيرفر
    dirs = ['core/models', 'apps/supplier_app/templates', 'static/css']
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, '__init__.py'), 'w') as f: pass

    # إنشاء ملف extensions.py إذا لم يوجد لكسر أخطاء الاستيراد
    ext_path = 'core/extensions.py'
    if not os.path.exists(ext_path):
        with open(ext_path, 'w') as f:
            f.write("from flask_sqlalchemy import SQLAlchemy\nfrom flask_login import LoginManager\ndb = SQLAlchemy()\nlogin_manager = LoginManager()")

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        try:
            # استيراد الموديل الجديد لتعميده
            from core.models.supplier_db import Supplier
            print("⚠️ جاري حذف الجداول القديمة...")
            db.drop_all() 
            print("💎 جاري بناء الجداول السيادية الجديدة...")
            db.create_all()
            print("✅ اكتمل التطهير.")
        except Exception as e:
            print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    start_over()
