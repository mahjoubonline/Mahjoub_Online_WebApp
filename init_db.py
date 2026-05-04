import os
from core import create_app, db
from sqlalchemy import text

# إنشاء نسخة من التطبيق للوصول إلى سياق قاعدة البيانات (سوقك الذكي)
app = create_app()

def initialize_database():
    with app.app_context():
        try:
            print("--------------------------------")
            print("🚀 جاري الاتصال بقاعدة البيانات وبناء الترسانة الرقمية لـ محجوب أونلاين...")
            
            # 1. استيراد الموديلات الموحدة لضمان التعرف عليها
            from core.models.user import User
            from core.models.vendor import Vendor 
            
            # 2. إنشاء الجداول الأساسية
            db.create_all()
            
            # 3. الترميم الهيكلي السيادي (Sovereign Structural Repair)
            # تنفيذ أوامر SQL مباشرة لضمان مطابقة الهيكل لمتطلبات المرحلة الثانية
            with db.engine.connect() as connection:
                print("🔍 فحص وتصحيح أعمدة الهوية والمالية...")
                
                # --- تحديث جدول المستخدمين (Users) ---
                connection.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT 'vendor';"))
                connection.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active_account BOOLEAN DEFAULT TRUE;"))
                
                # --- تحديث جدول الموردين (Vendors) للهوية MAH-963 ---
                connection.execute(text("ALTER TABLE vendors ADD COLUMN IF NOT EXISTS supplier_id VARCHAR(50) UNIQUE;"))
                connection.execute(text("ALTER TABLE vendors ADD COLUMN IF NOT EXISTS e_wallet VARCHAR(100) UNIQUE;"))
                
                # --- ضمان وجود أعمدة العملات الثلاث (YER, SAR, USD) ---
                connection.execute(text("ALTER TABLE vendors ADD COLUMN IF NOT EXISTS balance_yer FLOAT DEFAULT 0.0;"))
                connection.execute(text("ALTER TABLE vendors ADD COLUMN IF NOT EXISTS balance_sar FLOAT DEFAULT 0.0;"))
                connection.execute(text("ALTER TABLE vendors ADD COLUMN IF NOT EXISTS balance_usd FLOAT DEFAULT 0.0;"))
                
                # تأكيد كافة العمليات السيادية
                connection.commit()
            
            print("✅ تم فحص وترميم هيكل قاعدة البيانات بنجاح.")
            print("🌟 الترسانة الرقمية جاهزة الآن للتشغيل في بيئة Railway.")
            print("--------------------------------")
            
        except Exception as e:
            db.session.rollback()
            print("--------------------------------")
            print(f"❌ تعثرت عملية البناء السيادي: {str(e)}")
            print("💡 تأكد من صحة الاتصال بـ PostgreSQL في إعدادات الاستضافة.")
            print("--------------------------------")

if __name__ == "__main__":
    initialize_database()
