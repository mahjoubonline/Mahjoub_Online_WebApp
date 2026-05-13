from flask import Blueprint, render_template, session, redirect, url_for, flash
from models.supplier_db import Supplier
from functools import wraps

admin_bp = Blueprint('admin', __name__, template_folder='templates')

# 🛡️ بوابة الحماية السيادية (Decorator)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # التحقق من وجود معرف المستخدم في الجلسة
        if not session.get('user_id'):
            flash('تنبيه أمني: الدخول لغير المصرح لهم ممنوع. يرجى تسجيل الدخول أولاً.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required  # تطبيق البروتوكول الأمني
def dashboard():
    """
    مركز المراقبة الرئيسي لمنصة محجوب أونلاين.
    يتم جلب البيانات الحيوية من قاعدة البيانات لعرضها في واجهة القيادة.
    """
    try:
        # جلب إحصائيات الموردين لتعزيز هيبة لوحة التحكم
        suppliers_count = Supplier.query.count()
    except Exception:
        # في حال وجود خلل في الاتصال بقاعدة البيانات
        suppliers_count = 0

    # توجيه المؤسس إلى واجهة المحتوى المركزية مع البيانات السيادية
    return render_template(
        'admin/dashboard_content.html', 
        suppliers_count=suppliers_count,
        admin_name="علي محجوب"
    )
