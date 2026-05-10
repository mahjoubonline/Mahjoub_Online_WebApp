# core/security.py
import re
from functools import wraps
from flask import abort, redirect, url_for, flash, session, request
from flask_login import current_user

def admin_required(f):
    """حارس بوابة الإدارة: يسمح فقط لمن لديه رتبة admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash("عذراً، هذه المنطقة تتطلب صلاحيات قيادية عليا.", "danger")
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

def supplier_required(f):
    """حارس بوابة الموردين: يسمح فقط لمن لديه رتبة supplier"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'supplier':
            flash("هذه البوابة مخصصة للموردين المعتمدين فقط.", "warning")
            return redirect(url_for('supplier_panel.login'))
        return f(*args, **kwargs)
    return decorated_function

def sovereign_approval_required(f):
    """بروتوكول التعميد السيادي: يمنع الدخول حتى يتم تفعيل الحالة من الإدارة"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.role == 'supplier':
            # التحقق من الحالة في الموديل الجديد (pending, active, banned)
            if current_user.supplier_profile.status != 'active':
                flash("حسابك في حالة (قيد المراجعة) أو (محظور). يرجى التواصل مع الإدارة.", "info")
                return redirect(url_for('main.status_pending')) # صفحة انتظار مخصصة
        return f(*args, **kwargs)
    return decorated_function

# --- إضافات الترسانة الأمنية الجديدة ---

def sanitize_input(text):
    """تطهير النصوص من أي محاولات حقن برمجية (XSS Prevention)"""
    if not text: return ""
    # إزالة الأكواد البرمجية والرموز المشبوهة
    clean = re.sub(r'<.*?>', '', text)
    return clean.strip()

def secure_session():
    """تأمين الجلسة السيادية (تغيير معرف الجلسة عند كل دخول حساس)"""
    session.permanent = True
    session.modified = True
    # حماية ضد الهجمات التي تحاول سرقة الجلسة عبر الروابط
    if 'user_agent' not in session:
        session['user_agent'] = request.user_agent.string
    elif session['user_agent'] != request.user_agent.string:
        session.clear()
        return redirect(url_for('auth.login'))
