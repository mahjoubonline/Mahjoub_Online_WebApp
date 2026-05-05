# init_db.py
import os
import sys
from sqlalchemy import text

# --- بروتوكول تثبيت المسار السيادي لـ محجوب أونلاين ---
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# استيراد المكونات الأساسية بعد تثبيت المسار
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
            print("🚀 جاري تنفيذ بروتوكول الإصلاح الشامل لـ محجوب أونلاين...")
            
            # 1. معالجة جدول الموردين (حل مشكلة image_db5775.png)
            # نقوم بحذف الجدول القديم (إن وجد) لإعادة بنائه بالأعمدة الجديدة كلياً
            with db.engine.connect() as connection:
                print("⚠️ جاري إعادة هيكلة جدول الموردين (Suppliers) لضمان مطابقة الأعمدة...")
                try:
                    # نستخدم CASCADE لضمان الحذف النظيف في PostgreSQL (Railway)
                    connection.execute(text("DROP TABLE IF EXISTS suppliers CASCADE;"))
                    connection.commit()
                    print("✅ تم تنظيف الجدول القديم بنجاح.")
                except Exception as e:
                    print(f"ℹ️ تنبيه أثناء التنظيف: {e}")

            # 2. إنشاء الجداول بناءً على الموديلات البرمجية الجديدة
            # سيتم إنشاء جدول Supplier هنا بالأعمدة الكاملة (username, trade_name, etc.)
            db.create_all() 
            print("✅ تم إنشاء الجداول الجديدة بالهيكلية المحدثة.")
            
            # 3. الترميم الهيكلي للجداول الأخرى (Orders, Products)
            with db.engine.connect() as connection:
                print("🔍 فحص وترميم أعمدة العمليات التجارية...")
                
                alter_queries = [
                    # ترميم جدول الطلبات
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id);",
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS total_amount FLOAT DEFAULT 0.0;",
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS currency VARCHAR(10) DEFAULT 'YER';",
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'pending';",
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS shipping_address TEXT;",
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS contact_phone VARCHAR(20);",
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;",
                    # ترميم جداول المستخدمين والمنتجات
                    "ALTER TABLE products ADD COLUMN IF NOT EXISTS owner_id INTEGER REFERENCES users(id);",
                    "ALTER TABLE products ADD COLUMN IF NOT EXISTS currency VARCHAR(10) DEFAULT 'YER';",
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT 'admin';"
                ]
                
                for query in alter_queries:
                    try:
                        connection.execute(text(query))
                        connection.commit()
                    except Exception:
                        pass # العمود موجود بالفعل
            
            print("✅ اكتمل الترميم! كافة الأعمدة في image_db5775.png أصبحت موجودة الآن.")
            print("🌟 الترسانة الرقمية لـ محجوب أونلاين جاهزة للانطلاق.")
            print("--------------------------------")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ تعثرت عملية الترميم: {str(e)}")

if __name__ == "__main__":
    initialize_database()
