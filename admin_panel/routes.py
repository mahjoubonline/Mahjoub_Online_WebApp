import os
import random
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import logout_user, login_required, current_user
from sqlalchemy import text
from core import db 
from . import admin_bp
from .auth import handle_admin_login

# --- 1. استيراد النماذج (الهوية السيادية الموحدة) ---
# 🛡️ تم التعديل هنا: استيراد الكل من ملف user الموحد
from core.models.user import User, Vendor, WithdrawRequest

# محاولة استيراد النماذج الثانوية لتجنب الانهيار
try:
    from core.models.product import Product
except ImportError:
    Product = None

try:
    from core.models.business import Order
except ImportError:
    Order = None

# --- 2. خدمات الهوية والمحافظ السيادية ---
def generate_vendor_wallet():
    """توليد محفظة تبدأ بـ W-MAH لضمان الهوية المالية"""
    return f"W-MAH-{random.randint(100000, 999999)}"

def get_next_sovereign_id():
    """توليد المعرف السيادي MAH-963 بناءً على عدد الموردين الحاليين"""
    try:
        # حساب العدد الإجمالي للموردين المسجلين في القاعدة
        count = db.session.query(Vendor).count()
        return f"MAH-963{count + 1}"
    except Exception:
        db.session.rollback()
        return f"MAH-963{random.randint(100, 999)}"

# --- 3. تأمين الوصول والمصادقة ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if getattr(current_user, 'role', '') == 'admin':
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
    if getattr(current_user, 'role', '') != 'admin':
        flash("عذراً، لا تمتلك صلاحيات الوصول للترسانة الإدارية", "danger")
        return redirect(url_for('main.index'))
    
    stats = {
        'suppliers_count': db.session.query(Vendor).count(),
        'pending_withdrawals': db.session.query(WithdrawRequest).filter_by(status='pending').count(),
        'orders_count': db.session.query(Order).count() if Order else 0
    }
    return render_template('dashboard.html', **stats, show_repair=not session.get('repair_done'))

# --- 5. حوكمة الموردين (إضافة وتعميد مورد جديد) ---
@admin_bp.route('/add-supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    if getattr(current_user, 'role', '') != 'admin':
        return "Unauthorized", 403

    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            
            if User.query.filter_by(username=username).first():
                return jsonify({"status": "error", "message": "اسم المستخدم مسجل مسبقاً"}), 400

            # 1. إنشاء حساب الدخول
            new_user = User(username=username, role='vendor')
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.flush() 

            # 2. إنشاء بروفايل المورد بربط الهوية السيادية
            new_vendor = Vendor(
                user_id=new_user.id,
                supplier_id=request.form.get('next_id'),
                trade_name=request.form.get('trade_name'),
                owner_name=request.form.get('owner_name'),
                phone=request.form.get('phone'),
                e_wallet=request.form.get('e_wallet'),
                activity_type=request.form.get('activity_type'),
                province=request.form.get('province'),
                district=request.form.get('district'),
                balance_yer=0.0, balance_sar=0.0, balance_usd=0.0
            )
            
            db.session.add(new_vendor)
            db.session.commit()
            return jsonify({"status": "success", "message": "تم تعميد المورد بنجاح وربطه بالهوية MAH-963"})
            
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": f"فشل الحفظ: {str(e)}"}), 500

    return render_template('add_supplier.html', 
                           next_id=get_next_sovereign_id(), 
                           next_wallet=generate_vendor_wallet())

# --- 6. مسار الترميم الهيكلي (الطوارئ) ---
@admin_bp.route('/force-repair-now')
@login_required
def force_repair():
    if getattr(current_user, 'role', '') != 'admin':
        return "Unauthorized", 403
    try:
        # تنفيذ أوامر SQL مباشرة لضمان مطابقة الهيكل لمتطلبات محجوب أونلاين
        db.session.execute(text("ALTER TABLE vendors ADD COLUMN IF NOT EXISTS balance_yer FLOAT DEFAULT 0.0;"))
        db.session.execute(text("ALTER TABLE vendors ADD COLUMN IF NOT EXISTS balance_sar FLOAT DEFAULT 0.0;"))
        db.session.execute(text("ALTER TABLE vendors ADD COLUMN IF NOT EXISTS balance_usd FLOAT DEFAULT 0.0;"))
        db.session.commit()
        session['repair_done'] = True
        flash("تم تحديث الأرصدة السيادية الثلاثة بنجاح", "success")
        return redirect(url_for('admin.admin_dashboard'))
    except Exception as e:
        db.session.rollback()
        return f"Repair Error: {str(e)}"
