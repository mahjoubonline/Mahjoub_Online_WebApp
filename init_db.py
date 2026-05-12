import os
from flask import Flask
from core.extensions import db

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

    # 2. بناء قاعدة البيانات
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        try:
            # استيراد الموديلات لتعميدها
            from core.models.supplier_db import Supplier
            db.create_all()
            print("💎 تم بناء الجداول السيادية بنجاح.")
        except Exception as e:
            print(f"⚠️ تنبيه أثناء بناء الجداول: {e}")

if __name__ == "__main__":
    build_sovereign_infrastructure()
