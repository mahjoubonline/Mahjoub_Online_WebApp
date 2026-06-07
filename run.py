# coding: utf-8
# 📂 run.py (موجود في المجلد الرئيسي)

from apps import create_app, db
from apps.models.admin_db import AdminUser
from apps.models.supplier_db import Supplier
from werkzeug.security import generate_password_hash

app = create_app()

def seed_database():
    with app.app_context():
        # فحص ذكي: هل قاعدة البيانات فارغة؟
        if not AdminUser.query.first():
            print("🌱 اكتشاف قاعدة بيانات فارغة... جاري الزرع الأولي.")
            
            # 1. إضافة المالك: علي محجوب
            admin = AdminUser(username='ali_mahjoub', role='Owner', phone_number='0000000000')
            admin.set_password('123')
            db.session.add(admin)
            
            # 2. إضافة الـ 21 مورداً
            # تم دمج بياناتك هنا مباشرة لضمان تنفيذها
            suppliers_list = [
                {'username': f'sup_{i}', 'trade_name': f'مؤسسة مورد رقم {i}', 'owner_phone': f'7700000{i:02d}'}
                for i in range(1, 22)
            ]
            
            for data in suppliers_list:
                s = Supplier(username=data['username'], password_hash=generate_password_hash('sup_pass_123'))
                s.trade_name = data['trade_name']
                s.owner_phone = data['owner_phone']
                db.session.add(s)
            
            db.session.commit()
            print("✅ تم زرع المالك (علي محجوب) والـ 21 مورداً بنجاح.")

if __name__ == "__main__":
    # تشغيل عملية الزرع قبل بدء التطبيق
    seed_database()
    app.run()
