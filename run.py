# coding: utf-8
import os
from apps import create_app
from apps.extensions import db
from sqlalchemy import text, inspect

# إنشاء التطبيق
app = create_app()

def auto_fix_database():
    """
    دالة فحص وإصلاح هيكل قاعدة البيانات تلقائياً.
    تُنفذ عند الإقلاع لضمان وجود كافة الأعمدة المطلوبة في Postgres.
    """
    with app.app_context():
        try:
            print("🔧 جاري فحص هيكل قاعدة البيانات (Auto-Fix)...")
            inspector = inspect(db.engine)
            
            # الجداول التي نريد فحصها
            tables_to_check = {
                'supplier_wallets': ['_yer_total', '_sar_total', '_usd_total'],
                'wallet_transactions': ['_amount', '_profit_margin', '_notes']
            }
            
            for table_name, columns_needed in tables_to_check.items():
                if table_name in inspector.get_table_names():
                    existing_columns = [c['name'] for c in inspector.get_columns(table_name)]
                    for col in columns_needed:
                        if col not in existing_columns:
                            print(f"⚠️ العمود {col} مفقود في جدول {table_name}. جاري الإضافة...")
                            db.session.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {col} VARCHAR(255)"))
                            db.session.commit()
                            print(f"✅ تم إضافة {col} بنجاح.")
            
            print("🚀 قاعدة البيانات محدثة وجاهزة للعمل.")
        except Exception as e:
            print(f"❌ خطأ أثناء التحديث التلقائي: {str(e)}")
            db.session.rollback()

# استدعاء دالة الإصلاح قبل بدء السيرفر
auto_fix_database()

if __name__ == "__main__":
    # تشغيل التطبيق (استخدام PORT من Railway أو 5000 افتراضياً)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
