import os
from sqlalchemy import text
from core import create_app, db
from core.models.user import User

app = create_app()

def reset_and_build_database():
    """مسح الجداول القديمة وبناء الهيكل الجديد لضمان سيادة البيانات"""
    with app.app_context():
        try:
            print("🚨 جاري إعادة تهيئة الترسانة الرقمية للقاعدة...")
            
            # تنفيذ مسح شامل لجدول المستخدم لضمان تحديث الأعمدة (مثل role و is_active_account)
            db.session.execute(text('DROP TABLE IF EXISTS "user" CASCADE;'))
            db.session.commit()
            print("🗑️ تم مسح الجداول القديمة بنجاح.")
            
            # بناء الجداول من جديد بالمعايير العالمية للمرحلة الثانية
            db.create_all()
            print("🏗️ تم بناء الهيكل البرمجي الجديد بنجاح.")

            # تنصيب القائد "علي محجوب" كمسؤول أعلى للنظام
            admin_username = "علي محجوب"
            
            # التحقق من عدم وجود المستخدم مسبقاً لتجنب الأخطاء
            existing_admin = User.query.filter_by(username=admin_username).first()
            if not existing_admin:
                new_admin = User(
                    username=admin_username, 
                    role='admin' # تحديد الرصيد الإداري للقائد
                )
                new_admin.set_password('123') # سيتم تغييرها لاحقاً لتعزيز الأمان
                db.session.add(new_admin)
                db.session.commit()
                print(f"👑 تم تنصيب القائد {admin_username} في مركز المراقبة بنجاح.")
            else:
                print(f"ℹ️ القائد {admin_username} موجود بالفعل في النظام.")

        except Exception as e:
            db.session.rollback()
            print(f"❌ تعثرت عملية التهيئة بسبب: {str(e)}")

# تشغيل عملية الإصلاح لمرة واحدة لتهيئة بيئة العمل
# ملاحظة: يفضل تعطيل هذه الدالة بعد أول تشغيل ناجح في بيئة الإنتاج
reset_and_build_database()

if __name__ == "__main__":
    # إعدادات المنفذ للتوافق مع Railway/Render بمعايير عالمية
    port = int(os.environ.get("PORT", 8080))
    # التشغيل بدون Debug لضمان استقرار "محجوب أونلاين"
    app.run(host='0.0.0.0', port=port, debug=False)
