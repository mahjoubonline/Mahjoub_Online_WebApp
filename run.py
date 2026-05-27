# coding: utf-8
from apps import create_app
from apps.extensions import db
from sqlalchemy import text, inspect
import os

app = create_app()

def auto_fix_db():
    with app.app_context():
        try:
            print("🔧 جاري التحقق من هيكل قاعدة البيانات...")
            inspector = inspect(db.engine)
            if 'wallet_transactions' in inspector.get_table_names():
                columns = [c['name'] for c in inspector.get_columns('wallet_transactions')]
                
                # إضافة الأعمدة إذا كانت مفقودة
                if '_amount' not in columns:
                    db.session.execute(text("ALTER TABLE wallet_transactions ADD COLUMN _amount VARCHAR(255)"))
                    db.session.execute(text("ALTER TABLE wallet_transactions ADD COLUMN _profit_margin VARCHAR(255)"))
                    db.session.execute(text("ALTER TABLE wallet_transactions ADD COLUMN _notes VARCHAR(255)"))
                    db.session.commit()
                    print("✅ تم تحديث أعمدة قاعدة البيانات بنجاح.")
        except Exception as e:
            print(f"❌ فشل تحديث قاعدة البيانات: {e}")
            db.session.rollback()

# تشغيل وظيفة الإصلاح
auto_fix_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
