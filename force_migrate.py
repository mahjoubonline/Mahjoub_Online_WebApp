# 📂 force_migrate.py
from apps import create_app
from apps.extensions import db
from apps.models.supplier_db import Supplier

def force_update():
    app = create_app()
    with app.app_context():
        # هذا الأمر سيحذف الجدول القديم (الذي يسبب الخطأ) 
        # وينشئ جدولاً جديداً مطابقاً تماماً للكود الحالي
        db.drop_all() 
        db.create_all()
        print("✅ تم إعادة بناء قاعدة البيانات بنجاح.")

if __name__ == '__main__':
    force_update()
