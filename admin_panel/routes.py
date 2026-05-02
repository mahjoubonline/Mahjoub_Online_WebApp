import os
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import text
from core import db 

# استيراد النماذج بحذر شديد
try:
    from core.models.user import User
    from core.models.vendor import Vendor
except ImportError:
    User = None
    Vendor = None

try:
    from core.models.vendor import WithdrawRequest 
except ImportError:
    WithdrawRequest = None

from . import admin_bp
from .auth import handle_admin_login

# --- 1. مسار الطوارئ السيادي (إصلاح بدون تسجيل دخول) ---
@admin_bp.route('/force-repair-now')
def force_repair():
    """هذا المسار يعمل حتى لو كان النظام منهاراً لإصلاح قاعدة البيانات"""
    db.session.rollback()
    try:
        # تنفيذ الأمر مباشرة على المحرك لتجاوز أي مشاكل في الموديلات
        db.session.execute(text("ALTER TABLE vendors ADD COLUMN IF NOT EXISTS user_id INTEGER;"))
        db.session.commit()
        session['repair_done'] = True
        return """
        <div style="text-align:center; margin-top:50px; font-family:sans-serif;">
            <h1 style="color: #27ae60;">✅ تم تفعيل الترميم السيادي بنجاح!</h1>
            <p>قاعدة البيانات الآن متوافقة مع الهيكل الجديد.</p>
            <a href="/admin/dashboard" style="padding:10px 20px; background:#632C8F; color:white; text-decoration:none; border-radius:5px;">العودة للداشبورد</a>
        </div>
        """
    except Exception as e:
        db.session.rollback()
        return f"<h1 style='color:red;'>❌ فشل الإصلاح: {str(e)}</h1>"

# --- 2. نظام الإصلاح التلقائي (المحمي) ---
@admin_bp.route('/system-repair-sovereign')
@login_required
def auto_repair():
    db.session.rollback()
    try:
        db.session.execute(text("ALTER TABLE vendors ADD COLUMN IF NOT EXISTS user_id INTEGER;"))
        db.session.commit()
        session['repair_done'] = True 
        flash("تم تفعيل الترميم السيادي بنجاح.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"فشل الإصلاح: {str(e)}", "danger")
    return redirect(url_for('admin.admin_dashboard'))

# --- 3. بوابة الولوج السيادي ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    db.session.rollback()
    if current_user.is_authenticated:
        role = getattr(current_user, 'role', None)
        if role == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
    return handle_admin_login()

# --- 4. لوحة التحكم المركزية (الداشبورد) ---
@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    db.session.rollback()
    
    stats = {
        'suppliers_count': 0,
        'pending_withdrawals': 0,
        'orders_count': 0,
        'total_balance': "0.00"
    }

    show_repair = not session.get('repair_done', False)

    try:
        if Vendor:
            stats['suppliers_count'] = db.session.query(Vendor).count()
        if WithdrawRequest:
            stats['pending_withdrawals'] = db.session.query(WithdrawRequest).filter_by(status='pending').count()
    except Exception as e:
        db.session.rollback()
        show_repair = True 
        print(f"⚠️ Dashboard SQL Error: {str(e)}")

    return render_template('dashboard.html', 
                           suppliers_count=stats['suppliers_count'],
                           pending_withdrawals=stats['pending_withdrawals'],
                           orders_count=stats['orders_count'],
                           total_balance=stats['total_balance'],
                           show_repair=show_repair)

# --- 5. تسجيل الخروج ---
@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('تم إغلاق الجلسة الآمنة.', 'info')
    return redirect(url_for('admin.login'))
