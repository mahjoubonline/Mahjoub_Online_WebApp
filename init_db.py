import os
from core import create_app, db
from sqlalchemy import text

# إنشاء نسخة من التطبيق للوصول إلى سياق قاعدة البيانات
app = create_app()

def initialize_database():
    with app.app_context():
        try:
            print("جاري الاتصال بقاعدة البيانات وبناء الترسانة الرقمية...")
            
            # 1. استيراد الموديلات صراحة لضمان أن SQLAlchemy يراها
            from core.models.user import User
            from core.models.vendor import Vendor # تأكد من اسم الموديل (Vendor/Supplier)
            from core.models.product import Product
            
            # 2. إنشاء الجداول التي لا توجد أصلاً
            db.create_all()
            
            # 3. خطوة "الترميم الهيكلي" - إضافة الأعمدة الناقصة يدوياً لضمان التوافق
            # نقوم بفتح اتصال مباشر لتنفيذ أوامر SQL السيادية
            with db.engine.connect() as connection:
                print("🔍 فحص سلامة الهيكل الهيكلي للمستخدمين...")
                # إضافة عمود الصلاحيات إذا لم يوجد
                connection.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT 'admin';"))
                # إضافة عمود حالة الحساب إذا لم يوجد
                connection.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active_account BOOLEAN DEFAULT TRUE;"))
                
                # تأكيد التغييرات
                connection.commit()
            
            print("--------------------------------")
            print("✅ تم فحص وتحديث هيكل الترسانة الرقمية بنجاح.")
            print("🚀 منصة محجوب أونلاين جاهزة للعمل.")
            print("--------------------------------")
            
        except Exception as e:
            # في حال الفشل، نقوم بعمل rollback لمنع تعليق قاعدة البيانات
            db.session.rollback()
            print("--------------------------------")
            print(f"❌ حدث خطأ أثناء بناء أو ترميم قاعدة البيانات: {e}")
            print("💡 نصيحة: تأكد من أن متغير DATABASE_URL صحيح في Railway.")
            print("--------------------------------")

if __name__ == "__main__":
    initialize_database()
