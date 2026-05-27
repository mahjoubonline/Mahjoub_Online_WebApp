# coding: utf-8
import os
from apps import create_app
from apps.extensions import db
from sqlalchemy import text, inspect

app = create_app()

def auto_fix_database():
    """دالة الإصلاح الذاتي لهيكل قاعدة البيانات عند الإقلاع"""
    with app.app_context():
        try:
            print("🔧 جاري فحص هيكل قاعدة البيانات لضمان توافقها...")
            inspector = inspect(db.engine)
            
            # الجداول والأعمدة التي يجب أن تكون موجودة
            required_structure = {
                'supplier_wallets': ['_yer_total', '_sar_total', '_usd_total'],
                'wallet_transactions': ['_amount', '_profit_margin', '_notes']
            }
            
            for table_name, columns in required_structure.items():
                if table_name in inspector.get_table_names():
                    existing_cols = [c['name'] for c in inspector.get_columns(table_name)]
                    for col in columns:
                        if col not in existing_cols:
                            print(f"⚠️ إضافة العمود المفقود: {col} إلى جدول {table_name}")
                            # إضافة العمود بـ VARCHAR(255) ليتوافق مع التشفير
                            db.session.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {col} VARCHAR(255)"))
            
            db.session.commit()
            print("🚀 قاعدة البيانات محدثة وجاهزة للعمل.")
        except Exception as e:
            print(f"❌ خطأ أثناء الإصلاح التلقائي: {str(e)}")
            db.session.rollback()

# استدعاء دالة الإصلاح قبل تشغيل التطبيق
auto_fix_database()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
