import os
from sqlalchemy import text
from core import create_app, db
from core.models.user import User

# 1. إنشاء التطبيق (البلوبرنت يتم تسجيله تلقائياً داخل create_app)
app = create_app()

def reset_and_build_database():
    """مسح الجداول القديمة وبناء الهيكل الجديد لضمان سيادة البيانات"""
    with app.app_context():
        try:
            print("🚨 جاري فحص الترسانة الرقمية للقاعدة...")
            
            # فحص وجود الجداول قبل المسح لتجنب الأخطاء في التشغيل المتكرر
            db.session.execute(text('DROP TABLE IF EXISTS "user" CASCADE;'))
            db.session.commit()
            
            # بناء الجداول من جديد بالمعايير العالمية للمرحلة الثانية
            db.create_all()
            print("🏗️ تم بناء الهيكل البرمجي بنجاح.")

            # تنصيب القائد "علي محجوب" كمسؤول أعلى للنظام
            admin_username = "علي محجوب"
            existing_admin = User.query.filter_by(username=admin_username).first()
            
            if not existing_admin:
                new_admin = User(
                    username=admin_username, 
                    role='admin' 
                )
                new_admin.set_password('123') 
                db.session.add(new_admin)
                db.session.commit()
                print(f"👑 تم تنصيب القائد {admin_username} بنجاح.")
            
        except Exception as e:
            db.session.rollback()
            print(f"⚠️ ملاحظة: استمر السيرفر رغم تعثر التهيئة الجزئي: {str(e)}")

# تنفيذ التهيئة عند تشغيل الملف مباشرة
# وضعناها خارج __main__ لضمان تنفيذها عند استدعاء Gunicorn للتطبيق
with app.app_context():
    # يمكنك تفعيل السطر التالي إذا كنت تريد مسح البيانات في كل مرة ترفع فيها كود جديد
    # reset_and_build_database() 
    db.create_all() # هذا السطر يضمن وجود الجداول دون مسح البيانات القديمة

if __name__ == "__main__":
    # الحصول على المنفذ من بيئة Railway
    # Railway يستخدم غالباً المنفذ 5000 أو متغير PORT ديناميكي
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
