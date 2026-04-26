import os
from core import create_app, db

# 1. إنشاء نسخة التطبيق عبر دالة المصنع
app = create_app()

# 2. إدارة قاعدة البيانات وإنشاء الحسابات السيادية
with app.app_context():
    try:
        # ⚠️ الإجراء الجراحي: مسح شامل لضمان تطابق الحقول الجديدة (q_product_id, currency, wallets)
        # سيتم مسح قاعدة البيانات القديمة تماماً لإنهاء أي تعارض في الهيكل
        db.drop_all() 
        
        # إنشاء الجداول بناءً على الهيكل السيادي المطور (يشمل الآن ربط قمرة)
        db.create_all()
        print("✅ [Database] تم تصفير الهيكل ومزامنة الأعمدة الجديدة (q_product_id) بنجاح.")

        # استيراد الموديلات لضمان تسجيلها في الجلسة الحالية
        from core.models.user import User
        from core.models.supplier import Supplier
        from core.models.product import Product
        
        # --- إنشاء حساب القائد السيادي (Admin) ---
        admin_username = 'علي محجوب'
        if not User.query.filter_by(username=admin_username).first():
            new_admin = User(
                username=admin_username, 
                password='123', 
                role='admin'
            )
            db.session.add(new_admin)
            print(f"👤 [Security] تم تعميد حساب القائد '{admin_username}'.")

        # --- إنشاء حساب شريك النجاح (المورد العربي المطور) ---
        supplier_display_name = 'مورد تجريبي'
        if not Supplier.query.filter_by(name=supplier_display_name).first():
            test_supplier = Supplier(
                name=supplier_display_name, 
                email='test@supplier.com',
                password='123',
                activity_type='إلكترونيات وتقنية',
                trade_name='ترسانة محجوب الرقمية',
                full_name='علي محجوب (تجريبي)',
                province='الحديدة',
                district='الخوخة',
                phone='777777777',
                fin_type='banks',
                bank_name='بنك الكريمي الإسلامي',
                bank_acc='MAH-ACC-9046',
                is_approved=True, 
                status='active',
                # المحفظة المالية السيادية
                wallet_balance=100.0,
                wallet_usd=50.0,
                wallet_sar=150.0,
                wallet_yer=35000.0
            )
            db.session.add(test_supplier)
            db.session.flush() # للحصول على ID المورد قبل الإضافة التالية

            # --- إضافة منتج تجريبي مرتبط بـ "قمرة" كاختبار للربط ---
            test_product = Product(
                name="منتج تجريبي سيادي",
                q_product_id="Q-TEST-9046", # معرف وهمي للاختبار
                cost_price=10.0,
                currency="USD",
                status="active",
                supplier_id=test_supplier.id
            )
            db.session.add(test_product)
            print(f"📦 [Sourcing] تم إنشاء حساب المورد '{supplier_display_name}' ومنتج تجريبي بنجاح.")

        db.session.commit()
        print("✅ [System] تم حفظ جميع البيانات وتجهيز النظام السيادي للإقلاع.")

    except Exception as e:
        print(f"⚠️ [Critical] تنبيه أثناء الإقلاع السيادي: {e}")
        db.session.rollback()

if __name__ == "__main__":
    # 3. إعدادات المنفذ لـ Railway
    port = int(os.environ.get("PORT", 8080))
    
    # 4. الإقلاع الرسمي لمنصة محجوب أونلاين
    print(f"🚀 [Mahjoub Online] المنصة اللامركزية تعمل الآن على المنفذ {port}...")
    
    # ملاحظة: debug=False في الإنتاج (Railway)
    app.run(host='0.0.0.0', port=port, debug=False)
