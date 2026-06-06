# 📂 db_reset.py - مدير زراعة البيانات (21 مورد)
from apps import app, db
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import SupplierWallet
from werkzeug.security import generate_password_hash

def seed_data():
    with app.app_context():
        print("🌱 البدء في زراعة 21 مورد تجريبي...")
        
        for i in range(1, 22):
            try:
                # إنشاء المورد مع تعبئة كافة الحقول المطلوبة لضمان النجاح
                s = Supplier(
                    username=f"supplier_{i:02d}",
                    password_hash=generate_password_hash("password123"),
                    sovereign_id_enc=f"SID-{i:03d}",
                    status="قيد المراجعة",
                    rank_grade="ريادي"
                )
                
                # إسناد القيم للخصائص (Properties) التي تقوم بالتشفير والبحث
                s.trade_name = f"مورد تجريبي {i:02d}"
                s.owner_name = f"صاحب المورد {i:02d}"
                s.owner_phone = f"05000000{i:02d}"
                s.shop_phone = f"01000000{i:02d}"
                s.sovereign_id = f"SID-{i:03d}"
                s.wallet_code = f"WC-{i:03d}"
                
                db.session.add(s)
                db.session.flush() # توليد ID المورد
                
                # إنشاء المحفظة
                w = SupplierWallet(
                    supplier_id=s.id, 
                    balance_sar=100.0 * i, 
                    balance_yer=5000.0 * i, 
                    balance_usd=10.0 * i
                )
                db.session.add(w)
                db.session.commit()
                print(f"✅ تمت إضافة المورد: {s.username}")
                
            except Exception as e:
                print(f"⚠️ خطأ أثناء زراعة المورد {i}: {e}")
                db.session.rollback()
                
        print("🏁 اكتملت عملية زراعة الـ 21 مورداً بنجاح!")

if __name__ == "__main__":
    seed_data()
