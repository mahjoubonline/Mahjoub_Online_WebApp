from flask import session
from core.models.supplier import Supplier

def verify_supplier_credentials(username, password):
    """
    محرك التحقق السيادي: 
    تم تحسينه لضمان 'الارتباط الشرطي' بين المستخدم ونوع الحساب.
    """
    try:
        # 1. تنظيف المدخلات
        clean_username = username.strip() if username else ""
        
        # 2. البحث عن المورد (نستخدم الحقل الصحيح للمطابقة)
        supplier = Supplier.query.filter_by(name=clean_username).first()

        # 3. فحص الوجود
        if not supplier:
            return '⚠️ هذا الاسم غير مسجل في سجلات الموردين.', 'danger', None

        # 4. مطابقة كلمة المرور (بشكل صارم)
        if str(supplier.password).strip() != str(password).strip():
            return '❌ كلمة المرور السيادية غير صحيحة.', 'warning', None

        # 5. التوثيق (الختم الفوري)
        # نقوم بتنظيف الجلسة وتحديد النوع قبل إرجاع الكائن لضمان استجابة Flask-Login
        session.clear() # مسح شامل لأي أثر للأدمن قبل دخول المورد
        session.permanent = True
        session['user_type'] = 'supplier' 

        return f'✅ أهلاً بك يا {supplier.name}.. تم فتح الترسانة.', 'success', supplier

    except Exception as e:
        print(f"❌ [Logic Error]: {e}")
        return f'⚠️ عطل فني في بوابة العبور: {str(e)}', 'danger', None
