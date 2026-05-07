import os
import sys
from sqlalchemy import text
from werkzeug.security import generate_password_hash

# --- بروتوكول تثبيت المسار لضمان التعرف على الحزم داخل بيئة Railway ---
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from core import create_app, db
    from core.models.user import User
    from core.models.business import Order
    from core.models.product import Product
    from core.models.supplier import Supplier 
except ImportError as e:
    print(f"❌ خطأ في استيراد الموديلات: {e}")
    sys.exit(1)

app = create_app()

def initialize_database():
    """
    بروتوكول تهيئة قاعدة البيانات السيادية لمحجوب أونلاين.
    يتم تشغيل هذا الملف عند كل Deploy لبناء أو تحديث الهيكل.
    """
    with app.app_context():
        try:
            print("\n" + "="*40)
            print("🚀 بدء بروتوكول التحديث الشامل (Railway Edition)")
            print("="*40)
            
            # 1. تنظيف استباقي لجدول الموردين لضمان تحديث الهيكل الجغرافي
            with db.engine.connect() as connection:
                try:
                    # نستخدم CASCADE لضمان حذف القيود المرتبطة إن وجدت
                    connection.execute(text("DROP TABLE IF EXISTS suppliers CASCADE;"))
                    connection.commit()
                    print("✅ تم تصفير جدول الموردين (Fresh Start) لاستيعاب التحديثات.")
                except Exception as e:
                    print(f"⚠️ تنبيه أثناء تنظيف الجدول: {str(e)}")

            # 2. بناء كافة الجداول بناءً على الموديلات المحدثة
            # هذا السطر سيقوم بإنشاء أعمدة (province, district, tier) تلقائياً
            db.create_all() 
            print("✅ تم بناء هيكل الجداول الجديد بنجاح.")
            
            # 3. ترميم وتحديث أعمدة الجداول الحالية (أوامر سيادية للمسؤول)
            with db.engine.connect() as connection:
                alter_queries = [
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT 'admin';",
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'pending';"
                ]
                for query in alter_queries:
                    try:
                        connection.execute(text(query))
                        connection.commit()
                    except Exception: 
                        pass # إذا كان العمود موجوداً بالفعل سيتخطى الأمر
            print("✅ تم التأكد من سلامة أعمدة الصلاحيات والحالات.")

            # 4. زرع "مورد تجريبي" لاختبار فلاتر البحث والموقع فوراً
            # الموقع: الحديدة - الخوخة
            if not Supplier.query.filter_by(trade_name="مورد تجريبي").first():
                test_supplier = Supplier(
                    username="test_sup",
                    password="123",
                    trade_name="مورد تجريبي",
                    owner_name="علي محجوب",
                    phone="770000000",
                    province="الحديدة",
                    district="الخوخة",
                    status="active",
                    tier="ممتاز"
                )
                db.session.add(test_supplier)
                print("🧪 تم زرع المورد التجريبي (الخوخة) لاختبار نظام البحث.")

            # 5. تأمين حساب "علي محجوب" (السيادة المطلقة للمؤسس)
            # هذا الحساب هو مفتاح التحكم في المنصة
            admin_username = "علي محجوب"
            existing_admin = User.query.filter_by(username=admin_username).first()
            
            if not existing_admin:
                new_admin = User(
                    username=admin_username,
                    email='admin@mahjoub.online',
                    password=generate_password_hash('123', method='pbkdf2:sha256'),
                    role='admin'
                )
                db.session.add(new_admin)
                print(f"👤 تم إنشاء حساب المدير السيادي: {admin_username}")
            else:
                # تحديث الصلاحية للتأكد من أنه Admin
                existing_admin.role = 'admin'
                print(f"ℹ️ حساب المدير {admin_username} موجود مسبقاً وتَم التأكد من صلاحياته.")

            db.session.commit()
            print("\n🌟 الترسانة الرقمية جاهزة للعمل الآن.")
            print("="*40 + "\n")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ تعثر بروتوكول التهيئة بسبب: {str(e)}")
            print("تأكد من صحة DATABASE_URL في إعدادات Railway.\n")

if __name__ == "__main__":
    initialize_database()
