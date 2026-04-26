# --- المحرك السيادي للتحقق من الهوية - محجوب أونلاين ---
# الموقع: supplier_panel/auth_logic.py

from flask import session
from core.models.supplier import Supplier

def verify_supplier_credentials(username, password):
    """
    منطق التحقق الخاص بالمنصة اللامركزية لمحجوب أونلاين.
    هذا المحرك يفحص الهوية السيادية للمورد قبل السماح له بدخول الترسانة.
    
    المخرجات: (رسالة الحالة، صنف التنبيه، كائن المورد الموثق)
    """
    try:
        # 0. تطهير الجلسة السابقة (Identity Cleansing)
        # قبل البدء، نقوم بإزالة أي "وسم" قديم للأدمن لمنع التداخل البصري 
        # ولضمان أن النظام سيتعرف على المستخدم الحالي كـ "مورد" حصراً.
        session.pop('user_type', None)
        
        # 1. تطهير المدخلات (Data Sanitization)
        # نقوم بتنظيف الفراغات لضمان مطابقة دقيقة في قاعدة البيانات
        clean_username = username.strip() if username else ""
        
        # 2. الاستعلام عن الهوية السيادية
        # البحث يتم عبر حقل 'name' وهو المعرف الأساسي للمورد في النظام
        supplier = Supplier.query.filter_by(name=clean_username).first()

        # 3. فحص الوجود (Existence Check)
        if not supplier:
            return '⚠️ عذراً، هذا الاسم غير مسجل في المنصة اللامركزية لمحجوب أونلاين.', 'danger', None

        # 4. مطابقة مفاتيح الدخول (Password Verification)
        # يتم التحويل لنص لضمان عدم حدوث تعارض في الأنواع (Types) أثناء المقارنة
        stored_password = str(supplier.password).strip() if supplier.password else ""
        provided_password = str(password).strip() if password else ""

        if stored_password != provided_password:
            return '❌ كلمة المرور غير صحيحة، يرجى إعادة التثبت من مفاتيح الدخول.', 'warning', None

        # 5. التوثيق وتحديد المسار (Sovereign Session Labeling)
        # 🛡️ الختم السيادي: نخبر النظام رسمياً أن صاحب هذه الجلسة هو "مورد"
        # هذا السطر هو الضمان لمنع التوجيه التلقائي إلى لوحة التحكم الخاصة بالإدارة
        session.permanent = True
        session['user_type'] = 'supplier'

        # 6. النجاح المطلق والعبور
        return f'✅ مرحباً بك يا {supplier.name}.. تم التحقق من الهوية السيادية بنجاح.', 'success', supplier

    except Exception as e:
        # تسجيل العطل في مخرجات النظام (Terminal) للمراجعة الفنية من قبلك
        print(f"❌ [Logic Error] فشل في عملية التحقق السيادي: {e}")
        return f'⚠️ حدث خطأ تقني في نظام التحقق: {str(e)}', 'danger', None
