import os
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from sqlalchemy import text
from core import db 

# استيراد النماذج (تأكد من مطابقة الأسماء في مجلد core/models)
from core.models.user import User
from core.models.vendor import Vendor # النموذج الجديد الذي ظهر في الخطأ

try:
    from core.models.vendor import WithdrawRequest 
except ImportError:
    WithdrawRequest = None

from . import admin_bp
from .auth import handle_admin_login

# متغير للتحكم في ظهور رابط الإصلاح
SHOW_REPAIR_LINK = True

# --- 1. نظام الإصلاح التلقائي (لحل مشكلة العمود المفقود) ---
@admin_bp.route('/system-repair-sovereign')
@login_required
def auto_repair():
    global SHOW_REPAIR_LINK
    db.session.rollback()
    try:
        # إضافة العمود الذي تسبب في ظهور الخطأ 500
        db.session.execute(text("ALTER TABLE vendors ADD COLUMN IF NOT EXISTS user_id INTEGER;"))
        db.session.commit()
        SHOW_REPAIR_LINK = False
        flash("تم تفعيل الترميم السيادي.. الترسانة الآن مكتملة.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"فشل الإصلاح: {str(e)}", "danger")
    return redirect(url_for('admin.admin_dashboard'))

# --- 2. بوابة الولوج السيادي ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    db.session.rollback()
    # إذا كان علي محجوب مسجل دخول بالفعل، توجه للداشبورد
    if current_user.is_authenticated and getattr(current_user, 'role', None) == 'admin':
        return redirect(url_for('admin.admin_dashboard'))
    return handle_admin_login()

# --- 3. لوحة التحكم المركزية (الداشبورد) ---
@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    db.session.rollback() # تنظيف أي خطأ سابق لضمان تحميل الصفحة
    
    # إحصائيات افتراضية لضمان عدم انهيار الواجهة
    stats = {
        'suppliers_count': 0,
        'pending_withdrawals': 0,
        'orders_count': 0,
        'total_balance': "0.00"
    }

    try:
        # محاولة جلب البيانات الحقيقية من الترسانة
        stats['suppliers_count'] = Vendor.query.count()
        if WithdrawRequest:
            stats['pending_withdrawals'] = WithdrawRequest.query.filter_by(status='pending').count()
    except Exception as e:
        print(f"Database Alert: {str(e)}")
        db.session.rollback()
        # في حال الفشل، ستظل الإحصائيات 0 ويظهر زر الإصلاح

    return render_template('dashboard.html', 
                           **stats, 
                           show_repair=SHOW_REPAIR_LINK)

# --- 4. إدارة الموردين ---
@admin_bp.route('/suppliers')
@login_required
def manage_suppliers():
    db.session.rollback()
    suppliers = Vendor.query.all()
    return render_template('manage_suppliers.html', suppliers=suppliers)

# --- 5. تسجيل الخروج الآمن ---
@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('تم إغلاق الجلسة الآمنة للقيادة.', 'info')
    return redirect(url_for('admin.login'))
