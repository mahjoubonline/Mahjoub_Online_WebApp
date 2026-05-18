# run.py
# coding: utf-8
# 🚀 المحرك التنفيذي وفرمان الحوكمة الشاملة لمنصة محجوب أونلاين 2026
# التوثيق: سحق القيود المتعارضة قسرياً، تصفير الفضاء الرقمي، وتأمين النواة الموحدة

import os
from apps import create_app, db
from werkzeug.security import generate_password_hash
from sqlalchemy import text  # أداة تشغيل الاستعلامات البرمجية المباشرة

# 1. تشييد نسخة التطبيق الأساسية من المصنع المركزي
app = create_app()

def initialize_sovereignty():
    """
    دالة الإخضاع والتطهير المطلق:
    تفصل قيود المراجع الأجنبية رغماً عن قاعدة البيانات، وتسحق الجداول المتعارضة 
    لتوليد فضاء رقمي ناصع البياض يتوافق مع الأنظمة المالية الحديثة.
    """
    with app.app_context():
        try:
            print("⏳ جاري إرسال فرمان الإخضاع لـ PostgreSQL وتعطيل الفحص الهيكلي اللحظي...")
            
            # فتح الجلسة وتأجيل التحقق من قيود المفاتيح الأجنبية تماماً لكسر قفل الحذف
            db.session.execute(text("SET CONSTRAINTS ALL DEFERRED;"))
            
            # السحق التتابعي الشامل لكافة الجداول القديمة التي تسبب الأخطاء الداخلية
            print("🚨 جاري بدء السحق القسري للجداول المتعارضة عبر نظام CASCADE...")
            db.session.execute(text("DROP TABLE IF EXISTS wallet_transactions CASCADE;"))
            db.session.execute(text("DROP TABLE IF EXISTS supplier_wallets CASCADE;"))
            db.session.execute(text("DROP TABLE IF EXISTS wallets CASCADE;"))
            db.session.execute(text("DROP TABLE IF EXISTS suppliers CASCADE;"))
            db.session.commit()
            
            print("✨ تم تطهير الفضاء الرقمي لقاعدة البيانات بنجاح تام.")

            # استدعاء الموديلات محلياً لضمان توثيق العلاقات البرمجية الجديدة بشكل صحيح
            from apps.models.admin_db import AdminUser
            from apps.models.supplier_db import Supplier
            from apps.models.wallet_db import Wallet

            # إعادة بناء الهيكلية الموحدة النظيفة والمتوافقة مع كافة اللوحات
            print("⏳ جاري تشييد الجداول السيادية للمحافظ والموردين من نقطة الصفر...")
            db.create_all()
            
            # حقن ومواءمة الأعمدة اللوجستية لضمان عمل كافة التطبيقات الأخرى بمرونة
            print("🛡️ مواءمة حقول الحوكمة في جدول الموردين المحدث...")
            alter_query = """
            ALTER TABLE suppliers 
            ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'active',
            ADD COLUMN IF NOT EXISTS rank_grade VARCHAR(50) DEFAULT 'ريادي',
            ADD COLUMN IF NOT EXISTS registration_source VARCHAR(100) DEFAULT 'لوحة التحكم',
            ADD COLUMN IF NOT EXISTS created_by_id INTEGER,
            ADD COLUMN IF NOT EXISTS updated_by_id INTEGER,
            ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
            """
            db.session.execute(text(alter_query))
            db.session.commit()
            print("🚀 اكتمل بناء النواة الهيكلية ومواءمة جداول المنصة بالكامل.")
            
            # تأمين وتعمد حساب المالك والمؤسس الفعلي للمنصة
            owner = AdminUser.query.filter_by(username='علي محجوب').first()
            if not owner:
                print("🛡️ جاري تعميد حساب المالك الحوكمي للمنصة...")
                new_owner = AdminUser(
                    username='علي محجوب',
                    password_hash=generate_password_hash('123'),
                    role='Owner'
                )
                db.session.add(new_owner)
                db.session.commit()
                print("✅ تم تعميد 'علي محجوب' مالكاً سيادياً ومطلقاً للنظام الحوكمي.")
            else:
                print(f"📡 نظام الحوكمة مستقر: المالك السيادي '{owner.username}' متصل وقيد العمل.")
                
        except Exception as e:
            db.session.rollback()
            print(f"⚠️ تنبيه حرج: فشلت عملية التطهير القسري وإعادة التأسيس: {e}")

if __name__ == "__main__":
    # تنفيذ الفرمان الحوكمي بالتطهير والبناء النظيف قبل إقلاع السيرفر
    initialize_sovereignty()
    
    # التقاط المنفذ الديناميكي المخصص لبيئة تشغيل Railway
    port = int(os.environ.get("PORT", 5000))
    
    # إطلاق محرك المنصة السيادي للعمل الفوري
    app.run(host='0.0.0.0', port=port, debug=False)
