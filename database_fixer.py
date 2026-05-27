# database_fixer.py
from apps import create_app
from apps.extensions import db
from sqlalchemy import text

def run_fixer():
    app = create_app()
    with app.app_context():
        print("🔧 جاري تشغيل أداة إصلاح قاعدة البيانات...")
        try:
            # إضافة الأعمدة لجدول المعاملات
            db.session.execute(text("ALTER TABLE wallet_transactions ADD COLUMN IF NOT EXISTS _amount VARCHAR(255)"))
            db.session.execute(text("ALTER TABLE wallet_transactions ADD COLUMN IF NOT EXISTS _profit_margin VARCHAR(255)"))
            db.session.execute(text("ALTER TABLE wallet_transactions ADD COLUMN IF NOT EXISTS _notes VARCHAR(255)"))
            
            # إضافة الأعمدة لجدول المحافظ
            db.session.execute(text("ALTER TABLE supplier_wallets ADD COLUMN IF NOT EXISTS _yer_total VARCHAR(255)"))
            db.session.execute(text("ALTER TABLE supplier_wallets ADD COLUMN IF NOT EXISTS _sar_total VARCHAR(255)"))
            db.session.execute(text("ALTER TABLE supplier_wallets ADD COLUMN IF NOT EXISTS _usd_total VARCHAR(255)"))
            
            db.session.commit()
            print("✅ تم إصلاح الهيكل بنجاح!")
        except Exception as e:
            print(f"❌ حدث خطأ أثناء الإصلاح: {e}")

if __name__ == "__main__":
    run_fixer()
