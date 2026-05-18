# coding: utf-8
# 🚀 المحرك التنفيذي وفرمان الحوكمة الشاملة لمنصة محجوب أونلاين 2026

import os
from apps import create_app, db
from werkzeug.security import generate_password_hash

# 1. إنشاء نسخة التطبيق عبر المصنع المركزي
app = create_app()

def initialize_sovereignty():
    """
    دالة تعميد وتشييد البنية التحتية لعام 2026:
    تقوم بإنشاء كافة الجداول الناقصة مباشرة داخل سيرفر PostgreSQL الحي.
    """
    with app.app_context():
        try:
            print("⏳ جاري فحص وتعميد جداول النواة في السيرفر الحي...")
            
            # أمر التشييد الشامل والسيادي لجميع الجداول المستدعاة في الـ __init__
            db.create_all()
            db.session.commit()
            print("🚀 سيادة وحوكمة: تم فحص قاعدة البيانات وإنشاء الجداول بنجاح تنفيذي مطلق.")
            
            # تأمين حساب المؤسس والمالك السيادي للمنصة
            from apps.models.admin_db import AdminUser
            owner = AdminUser.query.filter_by(username='علي محجوب').first()
            if not owner:
                print("🛡️ جاري تعميد حساب المالك السيادي للمنصة...")
                new_owner = AdminUser(
                    username='علي محجوب',
                    password_hash=generate_password_hash('123'),
                    role='Owner'
                )
                db.session.add(new_owner)
                db.session.commit()
                print("✅ تم تعميد 'علي محجوب' مالكاً رسمياً لنظام الحوكمة الرقمية.")
                
        except Exception as e:
            db.session.rollback()
            print(f"⚠️ تنبيه تقني حرج: تعذر إنشاء الجداول على السيرفر الحي: {e}")

if __name__ == "__main__":
    # تنفيذ الفحص والإنشاء الآمن
    initialize_sovereignty()
    
    # تحديد المنفذ الخاص ببيئة Railway
    port = int(os.environ.get("PORT", 5000))
    
    # تشغيل محرك المنصة بنجاح
    app.run(host='0.0.0.0', port=port, debug=False)
