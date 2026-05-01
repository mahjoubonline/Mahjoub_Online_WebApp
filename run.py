# run.py
from core import create_app, db
from core.models.user import User

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        try:
            # 1. تحديث الهيكل (مهم جداً بعد حذف الإيميل)
            db.create_all()
            
            # 2. البحث عن المستخدم بدقة
            target_username = "علي محجوب"
            admin = User.query.filter_by(username=target_username).first()
            
            if not admin:
                print(f"🚀 البدء في إنشاء حساب القائد: {target_username}")
                # إنشاء الحساب بدون إيميل (كما عدلنا في الموديل)
                admin = User(
                    username=target_username,
                    role='admin',
                    is_active_account=True
                )
                admin.set_password('123')
                db.session.add(admin)
                db.session.commit()
                print(f"✅ تم بنجاح زرع حساب {target_username} في القاعدة.")
            else:
                # التأكد من تحديث كلمة المرور لـ 123 في حال كانت قديمة
                admin.set_password('123')
                admin.role = 'admin'
                db.session.commit()
                print(f"ℹ️ حساب {target_username} موجود مسبقاً وتم تحديث مفتاح التشفير.")
                
        except Exception as e:
            print(f"⚠️ فشل في تثبيت البيانات السيادية: {e}")

    # تشغيل المحرك
    app.run(host='0.0.0.0', port=8080)
