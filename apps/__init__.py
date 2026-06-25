# 2. زرع المورد (منفصل لمنع التأثير على الإدارة)
        try:
            from apps.models.supplier_db import Supplier
            # التحقق من وجود المورد
            if not Supplier.query.filter_by(username='mahjoub_store').first():
                # إنشاء مبدئي للمورد (بدون كود في البداية)
                new_supplier = Supplier(
                    username='mahjoub_store',
                    trade_name='متجر محجوب أونلاين',
                    phone='779077746',
                    search_phone='779077746'
                )
                new_supplier.set_password('123')
                db.session.add(new_supplier)
                db.session.commit() # الحفظ لأول مرة للحصول على ID فريد
                
                # الآن استدعاء الدالة التي ستولد supplier_code و تنشئ المحفظة وتخزنها
                new_supplier.generate_codes()
                db.session.commit() # الحفظ الثاني لتثبيت الكود والمحفظة
                
                print(f"✅ [Database Setup] تم زرع المورد بنجاح: {new_supplier.supplier_code}")
            else:
                print("ℹ️ [Database Setup] المورد موجود مسبقاً، تم تخطي الزرع.")
        except Exception as e:
            # الخطأ هنا لن يؤثر على عمل الإدارة
            print(f"⚠️ [Database Setup] خطأ في زرع المورد: {e}")
