import os
from core import create_app, db

# 1. إنشاء نسخة التطبيق عبر دالة المصنع
app = create_app()

# 2. إدارة قاعدة البيانات وإنشاء الحسابات الأولية
with app.app_context():
    try:
        # إنشاء الجداول أو تحديثها آلياً
        db.create_all()
        print("✅ [Database] تم مزامنة الجداول (الإدارة + الموردين + المحفظة) بنجاح.")

        # استيراد موديلات المستخدمين
        from core.models import User, Supplier
        
        # --- إنشاء حساب القائد السيادي (Admin) ---
        admin_username = 'علي محجوب'
        if not User.query.filter_by(username=admin_username).first():
            new_admin = User(
                username=admin_username, 
                password='123', 
                role='admin'
            )
            db.session.add(new_admin)
            db.session.commit()
            print(f"👤 [Security] تم إنشاء حساب القائد السيادي '{admin_username}' بنجاح.")
        else:
            print(f"ℹ️ [Security] حساب القائد '{admin_username}' موجود مسبقاً.")

        # --- إنشاء حساب شريك النجاح (المورد العربي) ---
        # ركز هنا: الاسم هو 'مورد تجريبي' ليتطابق مع ما يكتبه المورد في تسجيل الدخول
        supplier_display_name = 'مورد تجريبي'
        if not Supplier.query.filter_by(name=supplier_display_name).first():
            test_supplier = Supplier(
                name=supplier_display_name, 
                email='test@supplier.com', # سيبقى الإيميل مرجعاً في الخلفية فقط
                password='123',
                wallet_balance=100.0 # رصيد تجريبي لبدء العمل في الترسانة
            )
            db.session.add(test_supplier)
            db.session.commit()
            print(f"📦 [Sourcing] تم إنشاء حساب '{supplier_display_name}' بنجاح.")
        else:
            print(f"ℹ️ [Sourcing] حساب المورد العربي موجود وجاهز للاختبار.")

    except Exception as e:
        print(f"⚠️ [Database/Security] تنبيه أثناء الإقلاع: {e}")

if __name__ == "__main__":
    # 3. إعدادات المنفذ لـ Railway
    port = int(os.environ.get("PORT", 8080))
    
    # 4. الإقلاع الرسمي
    print(f"🚀 [Mahjoub Online] المنصة تعمل الآن على المنفذ {port}...")
    # debug=False ضروري جداً لضمان استقرار جلسات الدخول (Sessions)
    app.run(host='0.0.0.0', port=port, debug=False)
