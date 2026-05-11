import os
import sys
from sqlalchemy import text
from werkzeug.security import generate_password_hash

# --- 1. بروتوكول تثبيت المسار (Railway Infrastructure) ---
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from core import create_app, db
    from core.models.user import User
    from core.models.supplier import Supplier, SupplierStaff
except ImportError as e:
    print(f"❌ تعذر العثور على النواة (Core Models): {e}")
    sys.exit(1)

app = create_app()

def initialize_database():
    """
    بروتوكول الاقتحام النهائي - منصة محجوب أونلاين v4.0
    تحديث شامل لضمان الدخول بهوية 'admin' وتجاوز مشاكل الترميز العربي.
    """
    with app.app_context():
        try:
            print("\n" + "="*60)
            print("🚀 بدء بروتوكول الاقتحام والتعميد - محجوب أونلاين")
            print("="*60)
            
            # 1. بناء الهياكل الجديدة
            db.create_all() 
            print("✅ تم فحص وبناء الهياكل الجديدة (Tables Verified).")
            
            # 2. ترميم الأعمدة المفقودة
            with db.engine.connect() as connection:
                alter_queries = [
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS full_name VARCHAR(150);",
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR(20);",
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT 'admin';",
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;"
                ]
                for query in alter_queries:
                    try:
                        connection.execute(text(query))
                        connection.commit()
                    except Exception: 
                        pass
            print("✅ تم ترميم أعمدة الهوية (Fix Applied).")

            # 3. بروتوكول "تطهير الحسابات" لضمان الدخول
            # سنقوم بإنشاء/تحديث حسابين لضمان نجاحك في الدخول بأي منهما
            identities = [
                {"username": "admin", "full_name": "مدير النظام الأساسي"},
                {"username": "علي محجوب", "full_name": "المهندس علي محجوب"}
            ]

            for identity in identities:
                user = User.query.filter_by(username=identity['username']).first()
                if not user:
                    user = User(
                        username=identity['username'],
                        full_name=identity['full_name'],
                        email=f"{identity['username']}@mahjoub.online",
                        role='admin',
                        is_active=True
                    )
                    user.set_password('123')
                    db.session.add(user)
                    print(f"👤 تم إنشاء حساب جديد: {identity['username']}")
                else:
                    # تحديث الحساب الموجود لضمان الصلاحيات وكلمة المرور
                    user.role = 'admin'
                    user.is_active = True
                    user.set_password('123')
                    print(f"ℹ️ تم تحديث صلاحيات وكلمة مرور: {identity['username']}")

            db.session.commit()
            print("\n🌟 تم منح صلاحيات 'admin' لجميع الهويات بكلمة مرور: 123")
            print("="*60 + "\n")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ تعثر البروتوكول بسبب: {str(e)}")

if __name__ == "__main__":
    initialize_database()
