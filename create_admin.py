# create_admin.py
import os
import sys
from werkzeug.security import generate_password_hash

# تثبيت المسارات لضمان التعرف على المجلدات
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from core import create_app, db
    from core.models.user import User
except ImportError as e:
    print(f"❌ خطأ في النظام: {e}")
    sys.exit(1)

app = create_app()

def create_sovereign_admin():
    with app.app_context():
        # البيانات التي طلبتها بدقة
        admin_username = 'علي محجوب'
        admin_password = '123'
        
        # البحث عن الحساب لتجنب التكرار
        admin = User.query.filter_by(username=admin_username).first()
        
        if not admin:
            print(f"🚀 جاري إنشاء حساب: {admin_username}...")
            new_admin = User(
                username=admin_username,
                email='admin@mahjoub.online',
                # تشفير كلمة السر البسيطة لضمان أمان القاعدة
                password=generate_password_hash(admin_password, method='pbkdf2:sha256'),
                role='admin'
            )
            db.session.add(new_admin)
            db.session.commit()
            print(f"✅ تم إنشاء الحساب بنجاح!")
            print(f"👤 المستخدم: {admin_username}")
            print(f"🔑 كلمة السر: {admin_password}")
        else:
            print("ℹ️ الحساب موجود بالفعل.")

if __name__ == "__main__":
    create_sovereign_admin()
