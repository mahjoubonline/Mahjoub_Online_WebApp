import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# تعريف محلي مؤقت لكسر خطأ الاستيراد
db = SQLAlchemy()

def build_sovereign_infrastructure():
    print("🚀 بدء بروتوكول البناء التلقائي للهيكل النمطي...")
    
    # 1. قائمة المجلدات السيادية
    structure = [
        'core/models',
        'apps/supplier_app/templates',
        'apps/finance_app/templates',
        'apps/governance_app/templates',
        'static/css',
        'static/js'
    ]

    for path in structure:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            # إضافة ملف __init__.py لجعل المجلد حزمة برمجية
            init_file = os.path.join(path, '__init__.py')
            if not os.path.exists(init_file):
                with open(init_file, 'w') as f: pass
            print(f"✅ تم تأمين المسار: {path}")

    # 2. إنشاء ملف extensions.py تلقائياً إذا لم يوجد
    ext_path = 'core/extensions.py'
    if not os.path.exists(ext_path):
        with open(ext_path, 'w') as f:
            f.write("from flask_sqlalchemy import SQLAlchemy\nfrom flask_login import LoginManager\ndb = SQLAlchemy()\nlogin_manager = LoginManager()")
        print("✅ تم تخليق ملف extensions.py")

    # 3. بناء قاعدة البيانات (فقط إذا وجد ملف الموديل لاحقاً)
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    print("💎 اكتملت مرحلة التأسيس الهيكلي.")

if __name__ == "__main__":
    build_sovereign_infrastructure()
