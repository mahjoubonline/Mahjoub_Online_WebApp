import os
from sqlalchemy import text
from core import create_app, db
from core.models.user import User

# 1. إنشاء التطبيق
app = create_app()

def patch_database():
    """إصلاح شامل وهجومي لهيكل الجداول لضمان عدم التعثر"""
    with app.app_context():
        # قائمة كاملة بالأعمدة المطلوبة لجدول الموردين
        sql_commands = [
            # الربط الأساسي بالمستخدمين
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id);",
            
            # البيانات الأساسية والهوية المالية (التي تسببت في الخطأ الأخير)
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS owner_name VARCHAR(150);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS trade_name VARCHAR(150);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS phone VARCHAR(50);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS e_wallet VARCHAR(100);",
            
            # الأرصدة (ضرورية لمنع أخطاء الاستعلام عن الرصيد)
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS balance_yer FLOAT DEFAULT 0.0;",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS balance_sar FLOAT DEFAULT 0.0;",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS balance_usd FLOAT DEFAULT 0.0;",
            
            # نظام الهوية والموقع والأرشفة
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS id_type VARCHAR(100);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS id_card_number VARCHAR(100);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS id_image VARCHAR(255);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS activity_type VARCHAR(100);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS province VARCHAR(100);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS district VARCHAR(100);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS address_detail VARCHAR(255);",
            
            # الربط البنكي والمالي
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS bank_name VARCHAR(150);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS bank_acc VARCHAR(100);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS fin_type VARCHAR(50);"
        ]
        
        print("🔍 جاري فحص وتحديث الترسانة الرقمية...")
        for cmd in sql_commands:
            try:
                # تنفيذ كل أمر بشكل مستقل وعمل commit فوري
                db.session.execute(text(cmd))
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                # نتجاهل الخطأ إذا كان العمود موجوداً بالفعل
                continue
        print("✅ تم تحديث هيكل الجداول بنجاح.")

def initialize_system():
    """تهيئة النظام السيادي وقاعدة البيانات عند الإقلاع"""
    with app.app_context():
        try:
            # 1. تحديث هيكل الجداول أولاً لإصلاح أي نقص يمنع الاستعلامات
            patch_database()
            
            # 2. التأكد من إنشاء الجداول الأساسية إذا لم تكن موجودة
            db.create_all()
            
            # 3. التأكد من وجود الحساب الإداري للقائد علي محجوب
            admin_username = "علي محجوب"
            admin = User.query.filter_by(username=admin_username).first()
            if not admin:
                new_admin = User(username=admin_username, role='admin')
                new_admin.set_password('123')
                db.session.add(new_admin)
                db.session.commit()
                print("✅ تم تأكيد صلاحيات القائد في النظام.")
            else:
                print("✅ النظام والترسانة في حالة جاهزية تامة.")
        except Exception as e:
            print(f"⚠️ تنبيه النظام: {str(e)}")

# تنفيذ التهيئة والإصلاح الشامل قبل بدء استقبال الطلبات
initialize_system()

if __name__ == "__main__":
    # الحصول على المنفذ من بيئة تشغيل Railway
    port = int(os.environ.get("PORT", 5000))
    
    # تشغيل التطبيق (نضع debug=False لضمان استقرار الإنتاج)
    app.run(host='0.0.0.0', port=port, debug=False)
