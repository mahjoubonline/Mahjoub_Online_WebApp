# run.py
from apps import create_app
from apps.extensions import db
from sqlalchemy import text, inspect
import os

app = create_app()

def auto_fix_db():
    with app.app_context():
        try:
            # استخدام inspect للتحقق من هيكل الجدول
            inspector = inspect(db.engine)
            if 'wallet_transactions' in inspector.get_table_names():
                columns = [c['name'] for c in inspector.get_columns('wallet_transactions')]
                
                # قائمة الأعمدة الجديدة المطلوبة
                needed_cols = {'_amount': 'VARCHAR(255)', '_profit_margin': 'VARCHAR(255)', '_notes': 'TEXT'}
                
                for col_name, col_type in needed_cols.items():
                    if col_name not in columns:
                        print(f"🔧 جاري إضافة العمود المفقود: {col_name}")
                        db.session.execute(text(f"ALTER TABLE wallet_transactions ADD COLUMN {col_name} {col_type}"))
                
                db.session.commit()
                print("✅ تم فحص وتحديث قاعدة البيانات بنجاح.")
        except Exception as e:
            print(f"⚠️ خطأ أثناء التحديث التلقائي (قد يكون تم التحديث مسبقاً): {e}")
            db.session.rollback()

# تشغيل الإصلاح التلقائي
auto_fix_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
