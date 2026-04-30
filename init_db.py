import os
from core import create_app, db

# إنشاء نسخة من التطبيق للوصول إلى سياق قاعدة البيانات
app = create_app()

def initialize_database():
    with app.app_context():
        try:
            print("جاري الاتصال بقاعدة البيانات وبناء الترسانة الرقمية...")
            
            # استيراد الموديلات صراحة لضمان أن SQLAlchemy يراها قبل إنشاء الجداول
            from core.models.user import User
            from core.models.supplier import Supplier
            from core.models.product import Product
            
            # إنشاء الجداول
            db.create_all()
            
            print("--------------------------------")
            print("✅ تم بناء الترسانة بنجاح!")
            print("🚀 منصة محجوب أونلاين جاهزة للعمل.")
            print("--------------------------------")
            
        except Exception as e:
            print("--------------------------------")
            print(f"❌ حدث خطأ أثناء بناء قاعدة البيانات: {e}")
            print("--------------------------------")

if __name__ == "__main__":
    initialize_database()
