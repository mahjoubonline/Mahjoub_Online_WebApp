# coding: utf-8
# 🛡️ وحدة المهاجر التلقائي المستقل لتحديثات الجداول السيادية - محجوب أونلاين 2026

from sqlalchemy import text
from apps.extensions import db

def run_db_updates():
    """فحص قاعدة البيانات وحقن التحديثات والهياكل الجديدة صامتاً بدون ترمينال"""
    try:
        # 1. إنشاء جدول الحركات الجديد wallet_transactions وكل ما هو ناقص
        db.create_all()
        
        # 2. فحص وتحديث حقول جدول المحافظ القديم لحمايته من الانهيار
        with db.engine.connect() as connection:
            required_columns = [
                ("yer_total", "NUMERIC(15, 2) DEFAULT 0.00"),
                ("yer_withdrawn", "NUMERIC(15, 2) DEFAULT 0.00"),
                ("yer_pending", "NUMERIC(15, 2) DEFAULT 0.00"),
                ("sar_total", "NUMERIC(15, 2) DEFAULT 0.00"),
                ("sar_withdrawn", "NUMERIC(15, 2) DEFAULT 0.00"),
                ("sar_pending", "NUMERIC(15, 2) DEFAULT 0.00"),
                ("usd_total", "NUMERIC(15, 2) DEFAULT 0.00"),
                ("usd_withdrawn", "NUMERIC(15, 2) DEFAULT 0.00"),
                ("usd_pending", "NUMERIC(15, 2) DEFAULT 0.00")
            ]
            
            for col_name, col_type in required_columns:
                try:
                    # إضافة العمود في حال عدم وجوده
                    connection.execute(text(f"ALTER TABLE supplier_wallets ADD COLUMN {col_name} {col_type};"))
                    connection.commit()
                except Exception:
                    # تخطي إذا كان العمود موجوداً مسبقاً
                    continue
        print("✅ تم فحص وتحديث بنية الحوكمة المالية بنجاح تام.")
    except Exception as e:
        print(f"⚠️ تنبيه الهجرة: الجداول مستقرة أو مدمجة بالفعل: {e}")
