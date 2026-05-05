import os
from core import create_app, db
from sqlalchemy import text

# إنشاء نسخة من التطبيق للوصول إلى سياق قاعدة البيانات لـ محجوب أونلاين
app = create_app()

def initialize_database():
    with app.app_context():
        try:
            print("--------------------------------")
            print("🚀 جاري الاتصال وبناء الترسانة الرقمية لـ محجوب أونلاين...")
            
            # 1. استيراد الموديلات المحدثة لضمان التعرف عليها من قبل SQLAlchemy
            from core.models.user import User
            try:
                from core.models.business import Order
                from core.models.product import Product
            except ImportError:
                print("⚠️ تنبيه: تعذر استيراد بعض موديلات العمليات (Product/Order) حالياً.")
            
            # 2. إنشاء الجداول الأساسية المفقودة
            db.create_all()
            
            # 3. الترميم الهيكلي السيادي (Sovereign Structural Repair)
            with db.engine.connect() as connection:
                print("🔍 فحص وتصحيح أعمدة الهوية والمالية في الجداول الجديدة...")
                
                # --- تحديث جدول المستخدمين (Users) ---
                connection.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT 'admin';"))
                connection.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active_account BOOLEAN DEFAULT TRUE;"))
                
                # --- تحديث جدول المنتجات (Products) لربطها بـ owner_id بدلاً من المورد القديم ---
                connection.execute(text("ALTER TABLE products ADD COLUMN IF NOT EXISTS owner_id INTEGER REFERENCES users(id);"))
                connection.execute(text("ALTER TABLE products ADD COLUMN IF NOT EXISTS currency VARCHAR(10) DEFAULT 'YER';"))
                
                # --- تحديث جدول الطلبات (Orders) لضمان العملات الثلاث ---
                connection.execute(text("ALTER TABLE orders ADD COLUMN IF NOT EXISTS currency VARCHAR(10) DEFAULT 'YER';"))
                
                # تأكيد كافة العمليات السيادية في قاعدة البيانات
                connection.commit()
            
            print("✅ تم فحص وترميم هيكل قاعدة البيانات بنجاح.")
            print("🌟 الترسانة الرقمية جاهزة الآن للتشغيل في بيئة Railway.")
            print("--------------------------------")
            
        except Exception as e:
            db.session.rollback()
            print("--------------------------------")
            print(f"❌ تعثرت عملية البناء السيادي: {str(e)}")
            print("--------------------------------")

if __name__ == "__main__":
    initialize_database()
