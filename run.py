# 📂 run.py - نسخة الإنتاج ذاتية الإصلاح (Self-Healing)
import os
from apps import create_app
from apps.extensions import db
from apps.models.admin_db import AdminUser
from sqlalchemy import text

# 1. تهيئة التطبيق
app = create_app()

def auto_repair_db():
    """
    نظام الإصلاح التلقائي: يقوم بتحديث هيكل قاعدة البيانات 
    بشكل آمن عند كل عملية تشغيل (Deployment).
    """
    with app.app_context():
        try:
            # إنشاء الجداول الأساسية
            db.create_all()
            
            # إصلاح أعمدة جدول الموردين (Suppliers)
            db.session.execute(text("ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS search_name VARCHAR(150);"))
            db.session.execute(text("ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS search_phone VARCHAR(20);"))
            
            # إصلاح أعمدة جدول المحفظة (Supplier_Wallets)
            db.session.execute(text("ALTER TABLE supplier_wallets ADD COLUMN IF NOT EXISTS balance_sar FLOAT DEFAULT 0;"))
            db.session.execute(text("ALTER TABLE supplier_wallets ADD COLUMN IF NOT EXISTS balance_yer FLOAT DEFAULT 0;"))
            db.session.execute(text("ALTER TABLE supplier_wallets ADD COLUMN IF NOT EXISTS balance_usd FLOAT DEFAULT 0;"))
            
            # إصلاح أعمدة جدول معاملات المحفظة (Wallet_Transactions)
            db.session.execute(text("ALTER TABLE wallet_transactions ADD COLUMN IF NOT EXISTS currency VARCHAR(10) DEFAULT 'YER';"))
            db.session.execute(text("ALTER TABLE wallet_transactions ADD COLUMN IF NOT EXISTS description TEXT;"))
            db.session.execute(text("ALTER TABLE wallet_transactions ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'completed';"))
            
            db.session.commit()
            print("✅ نظام الإصلاح الذاتي: تم مزامنة هيكل الجداول بالكامل بنجاح.")
            
            # زرع الهوية السيادية
            u, p = "محجوب", "123"
            if not AdminUser.query.filter_by(username=u).first():
                new_admin = AdminUser(username=u, phone_number="0000000000", role='Owner')
                new_admin.set_password(p)
                db.session.add(new_admin)
                db.session.commit()
                print("✅ تم التأكد من وجود الهوية السيادية.")
                
        except Exception as e:
            print(f"🚨 خطأ في نظام الإصلاح التلقائي: {e}")
            db.session.rollback()

# تشغيل عملية الإصلاح قبل بداية السيرفر
auto_repair_db()

if __name__ == "__main__":
    # تشغيل السيرفر بالمنفذ المخصص أو الافتراضي
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
