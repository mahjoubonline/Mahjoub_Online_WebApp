import os
import sys
from sqlalchemy import text
from werkzeug.security import generate_password_hash

# --- بروتوكول تثبيت المسار لضمان التعرف على الحزم ---
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
    print(f"❌ خطأ في الاستيراد: {e}")
    sys.exit(1)

app = create_app()

def initialize_database():
    with app.app_context():
        try:
            print("--------------------------------")
            print("🚀 بدء بروتوكول التحديث الشامل لمحجوب أونلاين...")
            
            # 1. تنظيف جدول الموردين (لإعادة بناء الأعمدة الجغرافية والرتبة)
            with db.engine.connect() as connection:
                try:
                    connection.execute(text("DROP TABLE IF EXISTS suppliers CASCADE;"))
                    connection.commit()
                    print("✅ تم تصفير جدول الموردين لاستيعاب الفلاتر الجغرافية الجديدة.")
                except Exception:
                    pass

            # 2. بناء كافة الجداول (سيتم إنشاء أعمدة province, district, tier تلقائياً)
            db.create_all() 
            print("✅ تم بناء هيكل الجداول الجديد (المحافظات + الرتب).")
            
            # 3. ترميم الأعمدة المفقودة في الجداول الأخرى (أوامر سيادية)
            with db.engine.connect() as connection:
                alter_queries = [
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT 'admin';",
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'pending';"
                ]
                for query in alter_queries:
                    try:
                        connection.execute(text(query))
                        connection.commit()
                    except Exception: pass

            # 4. زرع "مورد تجريبي" لاختبار الفلاتر فوراً
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
                print("🧪 تم إضافة مورد تجريبي في (الخوخة) لاختبار الفلاتر.")

            # 5. حساب "علي محجوب" (السيادة المطلقة)
            admin_user = "علي محجوب"
            if not User.query.filter_by(username=admin_user).first():
                new_admin = User(
                    username=admin_user,
                    email='admin@mahjoub.online',
                    password=generate_password_hash('123', method='pbkdf2:sha256'),
                    role='admin'
                )
                db.session.add(new_admin)
                print(f"👤 تم تأمين حساب المدير: {admin_user}")

            db.session.commit()
            print("🌟 الترسانة الرقمية جاهزة تماماً.")
            print("--------------------------------")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ تعثرت العملية: {str(e)}")

if __name__ == "__main__":
    initialize_database()
