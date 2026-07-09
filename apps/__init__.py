# 📂 apps/__init__.py (تعديل استراتيجي)

def create_app():
    # ... (باقي كود الإعداد كما هو)

    with app.app_context():
        # استيراد الموديلات
        from apps.models import AdminUser
        
        # [تجاوز الإنشاء]: نستخدم inspect للتحقق من الحالة بدلاً من فرض البناء
        try:
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            # إذا لم تكن الجداول موجودة، نبنيها لمرة واحدة فقط
            if 'admin_users' not in existing_tables:
                print("ℹ️ [Setup]: الجداول غير موجودة، جاري الإنشاء...")
                db.create_all()
            else:
                print("✅ [Setup]: الجداول موجودة مسبقاً، تخطي البناء.")
        except Exception as e:
            print(f"⚠️ [Setup]: تحذير أثناء فحص الجداول: {e}")

        # [إضافة المالك بأمان مطلق]
        try:
            # نتأكد مرة أخرى من وجود الجدول قبل الاستعلام
            inspector = inspect(db.engine)
            if 'admin_users' in inspector.get_table_names():
                admin = AdminUser.query.filter_by(username='علي محجوب').first()
                if not admin:
                    owner = AdminUser(username='علي محجوب', role='Owner')
                    owner.set_password('123')
                    db.session.add(owner)
                    db.session.commit()
                    print("✅ [Setup]: تم إنشاء المستخدم المالك.")
            else:
                print("❌ [Setup]: جدول admin_users لا يزال مفقوداً!")
        except Exception as e:
            db.session.rollback()
            print(f"❌ [Setup]: خطأ أثناء إضافة المالك: {e}")

    return app
