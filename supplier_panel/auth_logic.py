from core.models import Supplier

def verify_supplier_credentials(username, password):
    """
    منطق التحقق الخاص بالمنصة اللامركزية
    النتيجة: (موجز الحالة، كود اللون، الكائن المسترجع)
    """
    # 1. البحث عن المورد في قاعدة البيانات
    supplier = Supplier.query.filter_by(name=username).first()

    # 2. فحص الوجود
    if not supplier:
        return "عذراً، هذا الاسم غير مسجل في المنصة اللامركزية.", "danger", None
    
    # 3. فحص كلمة المرور
    if supplier.password == password:
        return f"أهلاً بك يا {supplier.name}.. تم التحقق بنجاح.", "success", supplier
    else:
        return "كلمة المرور غير صحيحة، يرجى إعادة التثبت.", "warning", None
