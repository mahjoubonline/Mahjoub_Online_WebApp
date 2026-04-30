from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import admin_panel # استيراد البلوبرنت من الملف الذي صححناه
from core.models import User, Supplier, Product, db
from .utils import admin_required

# --- 1. بوابة الولوج (login.html) ---
@admin_panel.route('/login', methods=['GET', 'POST'])
def admin_login():
    # التحقق إذا كان المستخدم "علي محجوب" مسجل دخول مسبقاً
    if current_user.is_authenticated and getattr(current_user, 'role', None) == 'admin':
        return redirect(url_for('admin_panel.admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username, role='admin').first()

        if user and user.check_password(password):
            login_user(user)
            flash('تم تفعيل الولوج السيادي بنجاح.', 'success')
            return redirect(url_for('admin_panel.admin_dashboard'))
        else:
            flash('فشل في التحقق من الهوية.. تأكد من المعرف.', 'danger')

    return render_template('login.html')

# --- 2. لوحة التحكم المركزية (dashboard.html) ---
@admin_panel.route('/dashboard')
@login_required
@admin_required
def admin_dashboard():
    # إحصائيات المنصة لعام 2026
    stats = {
        's_count': Supplier.query.count(),
        'p_count': Product.query.count(),
        'orders_count': 0, 
        'total_balance': 0.00
    }
    return render_template('dashboard.html', **stats)

# --- 3. إدارة الموردين (manage_suppliers.html) ---
@admin_panel.route('/suppliers')
@login_required
@admin_required
def manage_suppliers():
    suppliers = Supplier.query.all()
    return render_template('manage_suppliers.html', suppliers=suppliers)

# --- 4. تسجيل الخروج ---
@admin_panel.route('/logout')
@login_required
def logout():
    logout_user()
    flash('تم إغلاق الجلسة الآمنة.', 'info')
    return redirect(url_for('admin_panel.admin_login'))
