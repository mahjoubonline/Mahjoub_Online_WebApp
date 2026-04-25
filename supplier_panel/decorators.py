from functools import wraps
from flask import render_template, redirect, url_for
from flask_login import current_user

def sovereign_approval_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 1. إذا لم يكن مسجلاً دخوله أصلاً، أعده لصفحة الدخول
        if not current_user.is_authenticated:
            return redirect(url_for('supplier_panel.login'))

        # 2. فحص الهوية: تأكد أن المستخدم "مورد" وليس "آدمن"
        # الأدمن لا يملك حقل is_approved، لذا نستخدم hasattr لتجنب الخطأ 500
        if hasattr(current_user, 'is_approved'):
            # إذا كان المورد غير معتمد (is_approved == False)
            if not current_user.is_approved:
                # نرسله فوراً لصفحة الانتظار (البرزخ)
                return render_template('waiting_approval.html')
        
        # 3. إذا كان معتمداً، اسمح له بدخول الدوشبورد
        return f(*args, **kwargs)
        
    return decorated_function
