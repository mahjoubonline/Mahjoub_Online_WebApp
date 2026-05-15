# coding: utf-8
from werkzeug.security import generate_password_hash
from apps import create_app, db
from apps.models.admin_db import AdminUser

app = create_app()

with app.app_context():
    # التحقق مما إذا كان الحساب موجوداً مسبقاً لمنع التكرار
    existing_user = AdminUser.query.filter_by(username='علي محجوب').first()
    
    if not existing_user:
        # إنشاء مستخدم الإدارة بكلمة سر مشفرة
        admin = AdminUser(
            username='علي محجوب',
            password_hash=generate_password_hash('123'), # تشفير كلمة السر 123
            role='Founder' # السيادة المطلقة للمؤسس
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ تم زرع حساب المؤسس (علي محجوب) بنجاح في قاعدة البيانات.")
    else:
        print("⚠️ حساب المؤسس موجود بالفعل في النظام.")
