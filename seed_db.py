# coding: utf-8
from apps import create_app, db
from apps.models.admin_db import AdminUser
from apps.models.supplier_db import Supplier
from werkzeug.security import generate_password_hash

app = create_app()

def seed_database():
    with app.app_context():
        # 1. إضافة المالك: علي محجوب
        admin = AdminUser.query.filter_by(username='ali_mahjoub').first()
        if not admin:
            admin = AdminUser(username='ali_mahjoub', role='Owner', phone_number='0000000000')
            admin.set_password('123') # سيتم تشفيرها بالدالة الموجودة في الموديل
            db.session.add(admin)
            print("✅ تم إضافة المالك: علي محجوب")

        # 2. إضافة الموردين الـ 21
        # يمكنك إضافة بيانات الموردين هنا في القائمة
        suppliers_data = [
            {'username': 'sup01', 'trade_name': 'مؤسسة النور', 'owner_phone': '770000001'},
            # ... أكمل إضافة الـ 21 مورد هنا ...
        ]

        for data in suppliers_data:
            if not Supplier.query.filter_by(username=data['username']).first():
                s = Supplier(username=data['username'], password_hash=generate_password_hash('sup_pass_123'))
                s.trade_name = data['trade_name']
                s.owner_phone = data['owner_phone']
                db.session.add(s)
        
        db.session.commit()
        print("🚀 تمت عملية الزرع بنجاح.")

if __name__ == '__main__':
    seed_database()
