from flask import Blueprint, redirect, url_for
from flask_login import login_required

# استيراد محرك الدخول فقط
# تأكد أن ملف auth.py يحتوي على دالة login_view كما في الكود السابق
from .auth import login_view 

# تعريف البلوبرنت الخاص بلوحة التحكم
admin_bp = Blueprint('admin', __name__, template_folder='templates')

# ==========================================
# بوابة الدخول السيادية (The Entry Point)
# ==========================================

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """توجيه طلب الدخول إلى المحرك المختص في auth.py"""
    return login_view()

# ==========================================
# بروتوكول الخروج الآمن (Logout)
# ==========================================

@admin_bp.route('/logout')
@login_required
def logout():
    """تأمين الخروج والعودة لبوابة الولوج"""
    from flask_login import logout_user
    logout_user()
    return redirect(url_for('admin.login'))
