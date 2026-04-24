import os
from core import create_app, db

# 1. إنشاء نسخة التطبيق عبر دالة المصنع
# هذه الدالة الآن تقوم بتسجيل بوابتي الإدارة والموردين معاً
app = create_app()

# 2. إدارة قاعدة البيانات وإنشاء الحساب السيادي وتحديث الهياكل
with app.app_context():
    try:
        # إنشاء الجداول أو تحديثها إذا تمت إضافة حقول جديدة (مثل wallet_balance)
        db.create_all()
        print("✅ [Database] تم مزامنة الجداول (الإدارة + الموردين + المحفظة) بنجاح.")

        # استيراد موديلات المستخدمين
        from core.models import User, Supplier
        
        # --- إنشاء حساب القائد "علي محجوب" ---
        admin_name = 'علي محجوب'
        if not User.query.filter_by(username=admin_name).first():
            new_admin = User(username=admin_name, password='123', role='admin')
            db.session.add(new_admin)
            db.session.commit()
            print(f"👤 [Security] تم إنشاء حساب القائد السيادي '{admin_name}' بنجاح.")
        else:
            print(f"ℹ️ [Security] حساب القائد '{admin_name}' موجود مسبقاً وجاهز للعمل.")

        # --- (اختياري) إنشاء مورد تجريبي لاختبار الربط والمحفظة ---
        test_supplier_email = 'test@supplier.com'
        if not Supplier.query.filter_by(email=test_supplier_email).first():
            test_supplier = Supplier(
                name='مورد تجريبي 1', 
                email=test_supplier_email, 
                password='123',
                wallet_balance=100.0 # رصيد تجريبي لبدء العمل
            )
            db.session.add(test_supplier)
            db.session.commit()
            print(f"📦 [Sourcing] تم إنشاء مورد تجريبي لاختبار نظام السحب الذكي.")

    except Exception as e:
        print(f"⚠️ [Database/Security] تنبيه أثناء الإقلاع: {e}")

if __name__ == "__main__":
    # 3. جلب المنفذ (Port) من Railway/Render
    # استخدام القيمة الافتراضية 8080 لتوافق الأنظمة السحابية
    port = int(os.environ.get("PORT", 8080))
    
    # 4. تشغيل السيرفر
    # تعطيل الـ Debug لضمان استقرار جلسات الدخول والـ Cookies في Railway
    print(f"🚀 Mahjoub Online is launching on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)
