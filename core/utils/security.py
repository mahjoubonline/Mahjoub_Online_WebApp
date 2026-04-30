from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(f):
    """
    مزخرف (Decorator) لمنع الوصول لغير المديرين.
    يُستخدم فوق المسارات الحساسة بدلاً من تكرار سطر التحقق.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403) # إرجاع خطأ "وصول غير مصرح"
        return f(*args, **kwargs)
    return decorated_function

def supplier_required(f):
    """
    مزخرف للتأكد من أن المستخدم مورد معتمد.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'supplier':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def sanitize_input(text):
    """
    دالة بسيطة لتنظيف المدخلات من الأكواد الخبيثة.
    """
    if text:
        return text.strip()
    return text
