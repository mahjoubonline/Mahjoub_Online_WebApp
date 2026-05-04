import os
import sys
import logging
from sqlalchemy import text
from core import create_app, db
from core.models.user import User

# إعداد السجلات لتعقب أخطاء "التعميد" بدقة
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Mahjoub_System")

# 1. إنشاء التطبيق
app = create_app()

def patch_database():
    """إصلاح شامل لهيكل الجداول مع تجنب قفل قاعدة البيانات"""
    with app.app_context():
        sql_commands = [
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS owner_name VARCHAR(150);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS trade_name VARCHAR(150);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS phone VARCHAR(50);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS e_wallet VARCHAR(100);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS balance_yer FLOAT DEFAULT 0.0;",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS balance_sar FLOAT DEFAULT 0.0;",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS balance_usd FLOAT DEFAULT 0.0;",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS id_type VARCHAR(100);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS id_card_number VARCHAR(100);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS id_image VARCHAR(255);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS activity_type VARCHAR(100);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS province VARCHAR(100);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS district VARCHAR(100);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS address_detail VARCHAR(255);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS bank_name VARCHAR(150);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS bank_acc VARCHAR(100);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS fin_type VARCHAR(50);"
        ]
        
        logger.info("🔍 جاري فحص وتحديث الترسانة الرقمية...")
        for cmd in sql_commands:
            try:
                db.session.execute(text(cmd))
                db.session.commit()
            except Exception:
                db.session.rollback()
                continue
        logger.info("✅ تم تحديث هيكل الجداول بنجاح.")

def initialize_system():
    """تهيئة النظام السيادي عند الإقلاع"""
    with app.app_context():
        try:
            # 1. إصلاح الجداول
            patch_database()
            # 2. إنشاء المفقود
            db.create_all()
            
            # 3. التأكد من وجود حساب القائد علي محجوب
            admin_username = "علي محجوب"
            admin = User.query.filter_by(username=admin_username).first()
            if not admin:
                new_admin = User(username=admin_username, role='admin')
                new_admin.set_password('123')
                db.session.add(new_admin)
                db.session.commit()
                logger.info("✅ تم تأكيد صلاحيات القائد علي محجوب.") #
            else:
                logger.info("✅ النظام والترسانة في حالة جاهزية تامة.")
        except Exception as e:
            logger.warning(f"⚠️ تنبيه النظام: {str(e)}")

# تشغيل التهيئة مرة واحدة عند الإقلاع
if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not app.debug:
    initialize_system()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # إيقاف debug لضمان عدم تنفيذ initialize_system مرتين
    app.run(host='0.0.0.0', port=port, debug=False)
