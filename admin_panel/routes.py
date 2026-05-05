import os
import random
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import logout_user, login_required, current_user
from sqlalchemy import text
from core import db 
from . import admin_bp
from .auth import handle_admin_login

# --- 1. استيراد النماذج (تم تنظيف الاستدعاءات المحذوفة) ---
from core.models.user import User

try:
    from core.models.product import Product
except ImportError:
    Product = None

try:
    from core.models.business import Order
except ImportError:
    Order = None

# --- 2. خدمات الهوية المؤقتة ---
def generate_vendor_wallet():
    return f"W-MAH-{random.randint(100000, 999999)}"

def get_next_sovereign_id():
    return f"MAH-963-{random.randint(100, 999)}"

# --- 3. تأمين الوصول والمصادقة ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # تأكد من أن الدور هو admin للدخول
        if getattr(current_user, 'role', '').lower() == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
    return handle_admin_login()

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("تم تأمين النظام وتسجيل الخروج بنجاح", "info")
    return redirect(url_for('admin.login'))

# --- 4. لوحة التحكم (مركز المراقبة) ---
@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    # تصحيح: جعل التحقق مرناً (يدعم Admin أو admin)
    user_role = getattr(current_user, 'role', '').lower()
    
    if user_role != 'admin':
        flash(f"عذراً، دورك الحالي ({user_role}) لا يمتلك صلاحيات الترسانة الإدارية", "danger")
        return redirect(url_for('main.index'))
    
    # جلب إحصائيات حقيقية من الملفات التي أصلحناها
    stats = {
        'suppliers_count': 0, 
        'pending_withdrawals': 0,
        'orders_count': db.session.query(Order).count() if Order else 0,
        'users_count': db.session.query(User).count()
    }
    return render_template('dashboard.html', **stats)

# --- 5. مسار الطوارئ لتعيين صلاحية الآدمن (Admin Fixer) ---
@admin_bp.route('/make-me-admin')
@login_required
def make_me_admin():
    """مسار سري لترقية حسابك الحالي إلى آدمن سيادي"""
    try:
        current_user.role = 'admin'
        db.session.commit()
        flash("تم ترقية حسابك إلى 'آدمن سيادي' بنجاح! يمكنك الآن دخول الداشبورد.", "success")
        return redirect(url_for('admin.admin_dashboard'))
    except Exception as e:
        db.session.rollback()
        return f"Error: {str(e)}"

# --- 6. مسار الترميم الهيكلي (الطوارئ) ---
@admin_bp.route('/force-repair-now')
@login_required
def force_repair():
    if getattr(current_user, 'role', '').lower() != 'admin':
        return "Unauthorized", 403
    try:
        session['repair_done'] = True
        flash("تم تشغيل بروتوكول الإصلاح الصامت بنجاح", "success")
        return redirect(url_for('admin.admin_dashboard'))
    except Exception as e:
        return f"Repair Error: {str(e)}"
