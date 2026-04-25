from functools import wraps
from flask import render_template
from flask_login import current_user

def sovereign_approval_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # التحقق السيادي: إذا كان المستخدم متصل ولكنه لم يحصل على الاعتماد بعد
        if current_user.is_authenticated and not current_user.is_approved:
            # عرض صفحة البرزخ (الانتظار)
            return render_template('waiting_approval.html')
        return f(*args, **kwargs)
    return decorated_function
