# run.py
import os
import logging
from sqlalchemy import text
from core import create_app, db
from core.models.user import User
from core.models.supplier import Supplier # الترسانة الجديدة

# إعداد السجلات السيادية
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Mahjoub_System")

app = create_app()

def patch_database():
    """تحديث هيكل الجداول ليتوافق مع التعديلات السيادية الجديدة"""
    with app.app_context():
        # قائمة التعديلات لضمان توافق الداتا القديمة مع الموديل الجديد
        sql_commands = [
            # تحديث جدول الموردين (الحقول الجديدة والمعدلة)
            "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS identity_type VARCHAR(50);", # بدلاً من id_type
            "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS identity_image_url VARCHAR(255);",
            "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS sovereign_id VARCHAR(100);",
            "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS tier VARCHAR(50) DEFAULT 'مورد مبتدئ';",
            "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS balance_yer NUMERIC(20, 2) DEFAULT 0.00;",
            "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS balance_sar NUMERIC(20, 2) DEFAULT 0.00;",
            "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS balance_usd NUMERIC(20, 2) DEFAULT 0.00;"
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
            # 1. إنشاء الجداول التي لم تكن موجودة
            db.create_all()
            
            # 2. إصلاح الأعمدة المفقودة
            patch_database()
            
            # 3. تأمين حساب القائد علي محجوب (Admin)
            admin_username = "علي محجوب"
            admin = User.query.filter_by(username=admin_username).first()
            if not admin:
                new_admin = User(username=admin_username, role='admin')
                new_admin.set_password('123') # سيتم تغييره لاحقاً
                db.session.add(new_admin)
                db.session.commit()
                logger.info(f"👤 تم إنشاء حساب القائد: {admin_username}") 
            else:
                logger.info(f"✅ القائد {admin_username} في مركز القيادة.")
                
        except Exception as e:
            logger.warning(f"⚠️ تنبيه النظام: {str(e)}")

# بروتوكول التشغيل (يمنع التكرار في وضع الـ Debug)
if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not app.debug:
    initialize_system()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
