# coding: utf-8
import os
from apps import create_app
from apps.extensions import db
from sqlalchemy import text

app = create_app()

def migrate_database_safely():
    """هذه الدالة تضمن وجود الأعمدة المطلوبة دون مسح بياناتك القديمة"""
    try:
        with app.app_context():
            print("🔄 جاري التحقق من سلامة هيكل قاعدة البيانات...")
            
            # 1. تحديث جدول الموردين (Suppliers)
            db.session.execute(text("ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS category VARCHAR(50) DEFAULT 'عام'"))
            db.session.execute(text("ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS behavior_score FLOAT DEFAULT 100.0"))
            db.session.execute(text("ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS total_transactions INTEGER DEFAULT 0"))
            db.session.execute(text("ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'pending'"))
            db.session.execute(text("ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS rank_grade VARCHAR(20) DEFAULT 'ريادي'"))
            db.session.execute(text("ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS registration_source VARCHAR(30) DEFAULT 'الموقع الخارجي'"))
            
            # 2. تحديث جدول المحافظ (Supplier Wallets)
            # لاحظ أننا نضيف الأعمدة بأسماء تبدأ بـ _ لتتطابق مع موديل التشفير الخاص بك
            db.session.execute(text("ALTER TABLE supplier_wallets ADD COLUMN IF NOT EXISTS _yer_total VARCHAR(255) DEFAULT '0.00'"))
            db.session.execute(text("ALTER TABLE supplier_wallets ADD COLUMN IF NOT EXISTS _sar_total VARCHAR(255) DEFAULT '0.00'"))
            db.session.execute(text("ALTER TABLE supplier_wallets ADD COLUMN IF NOT EXISTS _usd_total VARCHAR(255) DEFAULT '0.00'"))
            
            db.session.commit()
            print("✅ تم تحديث هيكل القاعدة بنجاح.")
    except Exception as e:
        print(f"⚠️ تحذير أثناء الإصلاح التلقائي: {e}")

# استدعاء دالة الإصلاح قبل بدء السيرفر
migrate_database_safely()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
