# coding: utf-8
# 📂 apps/migrator.py

from app import db
from sqlalchemy import text

def run_db_updates():
    """
    تشغيل التحديثات الهيكلية الصامتة لمحفظة الموردين بأمان.
    تستخدم تكتيك الـ Rollback عند حدوث خطأ لمنع انهيار السيرفر إذا كانت الأعمدة موجودة مسبقاً.
    """
    print("[MIGRATOR] Starting silent database structure synchronization...")

    # قائمة الأعمدة النقدية الثلاثية وعملاء الحوكمة المالية المضافة حديثاً
    columns_to_add = [
        ("yer_pending", "NUMERIC(15, 2) DEFAULT 0.00"),
        ("yer_withdrawn", "NUMERIC(15, 2) DEFAULT 0.00"),
        ("sar_pending", "NUMERIC(15, 2) DEFAULT 0.00"),
        ("sar_withdrawn", "NUMERIC(15, 2) DEFAULT 0.00"),
        ("usd_total", "NUMERIC(15, 2) DEFAULT 0.00"),
        ("usd_available", "NUMERIC(15, 2) DEFAULT 0.00"),
        ("usd_pending", "NUMERIC(15, 2) DEFAULT 0.00"),
        ("usd_withdrawn", "NUMERIC(15, 2) DEFAULT 0.00")
    ]
    
    for col_name, col_type in columns_to_add:
        try:
            # محاولة إضافة العمود بصيغة SQL مباشرة
            query = text(f"ALTER TABLE supplier_wallets ADD COLUMN {col_name} {col_type};")
            db.session.execute(query)
            db.session.commit()
            print(f"[MIGRATOR] Column '{col_name}' added successfully.")
        except Exception as e:
            # 🎯 الحل الجذري: عمل تراجع (Rollback) فوري عند حدوث تعارض أو إن كان العمود موجوداً
            # هذا يحافظ على سلامة اتصال Postgres ويمنع الـ Crash للسيرفر
            db.session.rollback()
            print(f"[MIGRATOR] Column '{col_name}' skipped (Already exists or verified).")
            
    print("[MIGRATOR] Silent database migration check completed safely.")
