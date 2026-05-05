import os
from flask import render_template, request, redirect, url_for, flash
from flask_login import logout_user, login_required, current_user
from sqlalchemy import text
from core import db 
from . import admin_bp
from .auth import handle_admin_login

# --- 1. بروتوكول التحقق السيادي (علي محجوب فقط) ---
# وظيفة لضمان أن الوصول مقتصر على رتبة 'admin' لضمان استقرار الهيكل الإداري
def is_admin_sovereign():
    return current_user.is_authenticated and getattr(current_user, 'role', '').lower() == 'admin'

# --- 2. بوابة الدخول (The Gateway) ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    هذه هي بوابة الدخول الرسمية.
    إذا كان النظام قد تعرف عليك بالفعل كـ 'Admin'، فسيتم توجيهك تلقائياً لمركز القيادة.
    """
    if is_admin_sovereign(): 
        return redirect(url_for('admin.admin_dashboard'))
    
    # استدعاء دالة المعالجة من ملف auth.py المسؤول عن التحقق من الهوية
    return handle_admin_login()

# --- 3. مركز القيادة (Dashboard) ---
@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    """
    المحرك المركزي لعرض الإحصائيات الحيوية للمنصة.
    """
    if not is_admin_sovereign():
        return redirect(url_for('main.index'))
    
    try:
        # استعلامات SQL مباشرة لضمان السرعة وتجنب أخطاء النماذج البرمجية (Models)
        suppliers = db.session.execute(text("SELECT COUNT(*) FROM users WHERE role = 'vendor'")).scalar() or 0
        total_users = db.session.execute(text("SELECT COUNT(*) FROM users")).scalar() or 0
        
        # حماية إضافية في حال كان جدول الطلبات قيد التحديث
        try:
            total_orders = db.session.execute(text("SELECT COUNT(*) FROM orders")).scalar() or 0
        except Exception:
            total_orders = 0

        stats = {
            'suppliers_count': suppliers,
            'orders_count': total_orders,
            'users_count': total_users,
            'pending_withdrawals': 0 
        }
        
        return render_template('dashboard.html', **stats)
        
    except Exception as e:
        # بروتوكول منع الانهيار (Fail-Safe)
        print(f"⚠️ Dashboard Crash Avoided: {str(e)}")
        return render_template('dashboard.html', suppliers_count=0, orders_count=0, users_count=0, pending_withdrawals=0)

# --- 4. إدارة الموردين (Vendor Management) ---
@admin_bp.route('/manage-suppliers')
@login_required
def manage_suppliers():
    """
    عرض والتحكم في حسابات الموردين (المعاز، الإلكترونيات، وغيرها)
    """
    if not is_admin_sovereign(): 
        return redirect(url_for('main.index'))
    
    try:
        result = db.session.execute(text("SELECT id, username, email, is_active_account FROM users WHERE role = 'vendor'"))
        suppliers = result.fetchall()
        return render_template('manage_suppliers.html', suppliers=suppliers)
    except Exception as e:
        flash(f"خلل في قاعدة البيانات: {str(e)}", "danger")
        return redirect(url_for('admin.admin_dashboard'))

# --- 5. إنهاء الجلسة (Logout) ---
@admin_bp.route('/logout')
@login_required
def logout():
    """
    إغلاق بوابة الوصول والعودة لصفحة تسجيل الدخول.
    """
    logout_user()
    flash("تم الخروج الآمن من نظام الإدارة", "info")
    return redirect(url_for('admin.login'))

# --- 6. مسارات التوسعة المستقبلية ---
@admin_bp.route('/add-supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    """
    إضافة كيان تجاري جديد لمنظومة محجوب أونلاين.
    """
    if not is_admin_sovereign(): 
        return redirect(url_for('main.index'))
    return render_template('add_supplier.html')
