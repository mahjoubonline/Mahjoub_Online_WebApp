import os
import sys
from sqlalchemy import text
from werkzeug.security import generate_password_hash

# --- 1. بروتوكول تثبيت المسار (Railway Infrastructure) ---
# نضمن أن السيرفر يرى مجلد core كحزمة برمجية متكاملة
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from core import create_app, db
    from core.models.user import User
    from core.models.supplier import Supplier
    # استيراد الموديلات الإضافية لضمان بناء الجداول المرتبطة
    try:
        from core.models.business import Order
        from core.models.product import Product
    except ImportError:
        Order = None
        Product = None
except ImportError as e:
    print(f"❌ تعذر العثور على النواة (Core Models): {e}")
    sys.exit(1)

app = create_app()

def initialize_database():
    """
    بروتوكول تهيئة الترسانة الرقمية لمحجوب أونلاين.
    يعمل هذا الملف على بناء الهيكل المالي والجغرافي وتأمين الوصول السيادي.
    """
    with app.app_context():
        try:
            print("\n" + "="*50)
            print("🚀 بدء بروتوكول التهيئة الشامل - منصة محجوب أونلاين")
            print("="*50)
            
            # 1. تنظيف استباقي (Fresh Start Protocol)
            # نقوم بحذف جدول الموردين فقط في حالة التحديث الجذري للهيكل
            with db.engine.connect() as connection:
                try:
                    # نستخدم CASCADE لضمان حذف كافة القيود (Constraints) المرتبطة
                    connection.execute(text("DROP TABLE IF EXISTS suppliers CASCADE;"))
                    connection.commit()
                    print("✅ تم تصفير جدول الموردين لاستيعاب الهيكل الجغرافي الجديد.")
                except Exception as e:
                    print(f"⚠️ ملاحظة أثناء التنظيف: {str(e)}")

            # 2. بناء الهيكل الرقمي (Schema Creation)
            # ينشئ كافة الجداول المعرفة في الموديلات (User, Supplier, etc.)
            db.create_all() 
            print("✅ تم بناء هيكل قاعدة البيانات (Tables Created).")
            
            # 3. ترميم الأعمدة المفقودة (Sovereign Alterations)
            with db.engine.connect() as connection:
                alter_queries = [
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT 'admin';",
                    "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS tier VARCHAR(50) DEFAULT 'مبتدئ';"
                ]
                for query in alter_queries:
                    try:
                        connection.execute(text(query))
                        connection.commit()
                    except Exception: 
                        pass # يتخطى إذا كان العمود موجوداً
            print("✅ تم التأكد من سلامة أعمدة الصلاحيات والرتب.")

            # 4. زرع المورد التجريبي (Testing The Arsenal)
            # الهدف: التأكد من عمل فلاتر "الحديدة - الخوخة" فور التشغيل
            test_sup_name = "مورد الخوخة التجريبي"
            if not Supplier.query.filter_by(trade_name=test_sup_name).first():
                test_supplier = Supplier(
                    username="khawkha_provider",
                    password="123", # كلمة مرور تجريبية
                    trade_name=test_sup_name,
                    owner_name="علي محجوب",
                    phone="770000000",
                    province="الحديدة",
                    district="الخوخة",
                    status="active",
                    tier="ممتاز",
                    balance_yer=100000.00, # رصيد افتتاحي للتيست
                    bank_name="بنك الكريمي",
                    bank_acc="1234567"
                )
                db.session.add(test_supplier)
                db.session.flush() # للحصول على ID
                test_supplier.mint_sovereign_id() # توليد المحفظة السيادية
                print(f"🧪 تم زرع مورد تجريبي في {test_supplier.district} لاختبار النظام.")

            # 5. تأمين حساب المؤسس "علي محجوب" (Absolute Sovereignty)
            admin_user = User.query.filter_by(username="علي محجوب").first()
            if not admin_user:
                new_admin = User(
                    username="علي محجوب",
                    email='admin@mahjoub.online',
                    password=generate_password_hash('123', method='pbkdf2:sha256'),
                    role='admin'
                )
                db.session.add(new_admin)
                print("👤 تم إنشاء حساب المدير السيادي (علي محجوب) بنجاح.")
            else:
                admin_user.role = 'admin'
                print("ℹ️ حساب المدير موجود مسبقاً وتَم تحديث صلاحياته.")

            db.session.commit()
            print("\n🌟 الترسانة الرقمية جاهزة للإقلاع الآن.")
            print("="*50 + "\n")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ تعثر بروتوكول التهيئة بسبب: {str(e)}")
            print("تأكد من إعدادات الاتصال في DATABASE_URL.\n")

if __name__ == "__main__":
    initialize_database()
