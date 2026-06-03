# 📂 inject_admin.py
from apps import create_app
from apps.extensions import db
from apps.models.admin_db import AdminUser

def inject_sovereign_admin(username, password, phone):
    app = create_app()
    with app.app_context():
        # التحقق مما إذا كان المستخدم موجوداً لتجنب التكرار
        existing = AdminUser.query.filter_by(username=username).first()
        if existing:
            print(f"⚠️ المستخدم {username} موجود مسبقاً. تم التخطي.")
            return

        # إنشاء المستخدم الجديد
        new_admin = AdminUser(
            username=username,
            phone_number=phone,
            role='Owner' # دور المالك السيادي
        )
        new_admin.set_password(password) # تشفير كلمة المرور عبر الموديل المحصن
        
        db.session.add(new_admin)
        db.session.commit()
        print(f"✅ تم حقن الهوية السيادية للمستخدم: {username}")

if __name__ == "__main__":
    # استبدل القيم هنا بما تريد
    inject_sovereign_admin("mahjoub", "YourSecurePassword2026", "0000000000")
