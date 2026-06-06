# 📂 seed_db.py
from apps import create_app
from apps.extensions import db
from apps.models.admin_db import AdminUser
from apps.models.supplier_db import Supplier # تأكد من المسار الصحيح

app = create_app()

def seed_system():
    with app.app_context():
        # 1. زرع المدير السيادي "محجوب"
        admin = AdminUser.query.filter_by(username="محجوب").first()
        if not admin:
            new_admin = AdminUser(username="محجوب", phone_number="0000000000", role='Owner')
            new_admin.set_password("123") # سيتم تشفيره عبر الدالة
            db.session.add(new_admin)
            print("✅ تم زرع المستخدم المالك (محجوب).")
        
        # 2. زرع الموردين (بشكل يمنع التكرار)
        suppliers = [
            {"name": "مورد أساسي 1", "phone": "0500000000"},
            {"name": "مورد أساسي 2", "phone": "0511111111"}
        ]
        for s in suppliers:
            if not Supplier.query.filter_by(name=s['name']).first():
                db.session.add(Supplier(name=s['name'], phone=s['phone']))
        
        db.session.commit()
        print("✅ تم زرع الموردين بنجاح.")

if __name__ == "__main__":
    seed_system()
