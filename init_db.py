import os
from core import create_app, db
from sqlalchemy import text

app = create_app()

def initialize_database():
    with app.app_context():
        try:
            print("--------------------------------")
            print("🚀 جاري تنفيذ بروتوكول الإصلاح الشامل لـ محجوب أونلاين...")
            
            # 1. ضمان وجود الجداول الأساسية
            from core.models.user import User
            from core.models.business import Order
            from core.models.product import Product
            
            db.create_all() # إنشاء الجداول الجديدة إن لم تكن موجودة
            
            # 2. الترميم الهيكلي العميق (Deep Structural Repair)
            with db.engine.connect() as connection:
                print("🔍 فحص وترميم أعمدة جدول الطلبات (Orders)...")
                
                # إضافة كافة الأعمدة المفقودة التي تسببت في الخطأ الظاهر بالصورة
                alter_queries = [
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id);",
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS total_amount FLOAT DEFAULT 0.0;",
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS currency VARCHAR(10) DEFAULT 'YER';",
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'pending';",
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS shipping_address TEXT;",
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS contact_phone VARCHAR(20);",
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;",
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;"
                ]
                
                for query in alter_queries:
                    try:
                        connection.execute(text(query))
                        print(f"✅ تم تنفيذ: {query[:30]}...")
                    except Exception as e:
                        print(f"⚠️ تنبيه (قد يكون العمود موجوداً): {str(e)[:50]}")
                
                # ترميم جدول المنتجات لضمان الرشاقة
                print("🔍 فحص وترميم أعمدة جدول المنتجات (Products)...")
                connection.execute(text("ALTER TABLE products ADD COLUMN IF NOT EXISTS owner_id INTEGER REFERENCES users(id);"))
                connection.execute(text("ALTER TABLE products ADD COLUMN IF NOT EXISTS currency VARCHAR(10) DEFAULT 'YER';"))
                
                # تعميد الآدمن السيادي
                connection.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT 'admin';"))
                
                connection.commit()
            
            print("✅ اكتمل الترميم! كافة الأعمدة أصبحت جاهزة للعمل.")
            print("🌟 الترسانة الرقمية جاهزة للانطلاق.")
            print("--------------------------------")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ تعثرت عملية الترميم: {str(e)}")

if __name__ == "__main__":
    initialize_database()
