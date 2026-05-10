from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required

# استيراد محرك الدخول من ملف auth.py المجاور
from .auth import login_view 

# تعريف البلوبرنت الخاص بلوحة التحكم
admin_bp = Blueprint('admin', __name__, template_folder='templates')

# ==========================================
# 1. بوابة الدخول (The Security Gate)
# ==========================================

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """توجيه طلب الدخول إلى المحرك المختص في auth.py"""
    return login_view()

# ==========================================
# 2. غرفة القيادة (The Dashboard)
# ==========================================

@admin_bp.route('/dashboard')
@login_required # لا يمكن الدخول هنا إلا بعد تجاوز بوابة الدخول
def dashboard():
    """عرض لوحة التحكم الرئيسية"""
    return render_template('admin/dashboard.html')

# ==========================================
# 3. بروتوكول الخروج الآمن (Logout)
# ==========================================

@admin_bp.route('/logout')
@login_required
def logout():
    """تأمين الخروج والعودة لبوابة الولوج"""
    from flask_login import logout_user
    logout_user()
    return redirect(url_for('admin.login'))
