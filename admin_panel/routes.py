import os
import re
import random
import string
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import text
from core import db 

# --- استيراد النماذج (استخدام المسميات التي كانت تعمل لضمان الاستقرار) ---
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

# --- الربط السيادي مع ملف الخدمات ---
try:
    from services.wallet_service import generate_wallet_id
except ImportError:
    def generate_wallet_id(next_id=None):
        if next_id:
            return f"W-{next_id}"
        return f"W-MAH-{random.randint(9000, 9999)}"

from . import admin_bp
from .auth import handle_admin_login

# دالة مساعدة لحساب المعرف التالي (MAH-XXXX)
def get_next_sovereign_id():
    try:
        db.session.rollback()
        count = db.session.query(Vendor).count()
        return f"MAH-963{count + 1}"
    except:
        return f"MAH-963{random.randint(1, 99)}"

# --- 1. مسار الطوارئ والترميم العميق (المحدث ليناسب قاعدة البيانات الحالية) ---
@admin_bp.route('/force-repair-now')
def force_repair():
    report = []
    try:
        db.session.rollback() 
        # تحديث جدول المستخدمين
        db.session.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT 'admin';"))
        db.session.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active_account BOOLEAN DEFAULT TRUE;"))
        report.append("✅ تم تحديث أدوار المستخدمين وصلاحيات الحسابات.")

        # تحرير الأعمدة القديمة وتأمين الجديدة في جدول vendors
        legacy_columns = ['vendor_uid', 'username', 'email', 'status']
        for col in legacy_columns:
            db.session.execute(text(f"ALTER TABLE vendors ADD COLUMN IF NOT EXISTS {col} VARCHAR(255);"))
            db.session.execute(text(f"ALTER TABLE vendors ALTER COLUMN {col} DROP NOT NULL;"))
            report.append(f"✅ تم تحرير العمود ({col}) من قيود الإدخال.")

        # إضافة أعمدة الأرصدة والمحفظة إذا لم تكن موجودة
        db.session.execute(text("ALTER TABLE vendors ADD COLUMN IF NOT EXISTS balance_yer FLOAT DEFAULT 0.0;"))
        db.session.execute(text("ALTER TABLE vendors ADD COLUMN IF NOT EXISTS balance_sar FLOAT DEFAULT 0.0;"))
        db.session.execute(text("ALTER TABLE vendors ADD COLUMN IF NOT EXISTS balance_usd FLOAT DEFAULT 0.0;"))
        db.session.execute(text("ALTER TABLE vendors ADD COLUMN IF NOT EXISTS user_id INTEGER;"))
        db.session.execute(text("ALTER TABLE vendors ADD COLUMN IF NOT EXISTS e_wallet VARCHAR(100);"))
        db.session.execute(text("ALTER TABLE vendors ADD COLUMN IF NOT EXISTS province VARCHAR(100);"))
        db.session.execute(text("ALTER TABLE vendors ADD COLUMN IF NOT EXISTS district VARCHAR(100);"))
        
        db.session.commit()
        session['repair_done'] = True

        report_items = "".join([f"<li style='margin-bottom:10px;'>{item}</li>" for item in report])
        return f"""
        <div style="max-width:600px; margin:50px auto; padding:30px; border-radius:15px; box-shadow:0 10px 25px rgba(0,0,0,0.1); font-family:sans-serif; direction:rtl; text-align:right; background:white; border-top: 5px solid #632C8F;">
            <h1 style="color: #632C8F;">✨ تقرير الترميم التلقائي</h1>
            <ul style="list-style:none; padding:20px 0; color:#333;">{report_items}</ul>
            <p style="color:green; font-weight:bold;">✅ تم تحديث القاعدة بنجاح! السيرفر الآن مستقر.</p>
            <a href="/admin/dashboard" style="display:inline-block; padding:12px 25px; background:#632C8F; color:white; text-decoration:none; border-radius:8px;">العودة لمركز القيادة</a>
        </div>
        """
    except Exception as e:
        db.session.rollback()
        return f"<div style='direction:rtl; text-align:center; padding:50px;'><h1 style='color:red;'>❌ فشل الترميم</h1><code>{str(e)}</code></div>"

# --- 2. لوحة التحكم المركزية ---
@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    try:
        db.session.rollback()
        stats = {'suppliers_count': 0, 'pending_withdrawals': 0, 'orders_count': 0}
        show_repair = not session.get('repair_done', False)

        if Vendor:
            stats['suppliers_count'] = db.session.query(Vendor).count()
        if WithdrawRequest:
            stats['pending_withdrawals'] = db.session.query(WithdrawRequest).filter_by(status='pending').count()
        
        return render_template('dashboard.html', **stats, show_repair=show_repair)
    except:
        db.session.rollback()
        return render_template('dashboard.html', suppliers_count=0, pending_withdrawals=0, show_repair=True)

# --- 3. حوكمة الموردين ---
@admin_bp.route('/add-supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    if request.method == 'POST':
        try:
            db.session.rollback()
            username = request.form.get('username')
            password = request.form.get('password')
            
            received_id = request.form.get('next_id') or get_next_sovereign_id()
            received_wallet = request.form.get('e_wallet') or generate_wallet_id(received_id)

            if User.query.filter_by(username=username).first():
                return jsonify({"status": "error", "message": f"اسم المستخدم ({username}) مسجل مسبقاً."})

            new_user = User(username=username, role='vendor')
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.flush() 

            new_vendor = Vendor(
                user_id=new_user.id,
                vendor_uid=received_id,
                owner_name=request.form.get('owner_name'),
                trade_name=request.form.get('trade_name'),
                phone=request.form.get('phone'),
                e_wallet=received_wallet,
                balance_yer=0.0, balance_sar=0.0, balance_usd=0.0,
                id_type=request.form.get('id_type'),
                id_card_number=request.form.get('id_card_number'),
                activity_type=request.form.get('activity_type'),
                province=request.form.get('province'),
                district=request.form.get('district'),
                address_detail=request.form.get('address_detail'),
                bank_name=request.form.get('bank_name'),
                bank_acc=request.form.get('bank_acc'),
                fin_type=request.form.get('fin_type')
            )
            db.session.add(new_vendor)
            db.session.commit()
            
            return jsonify({"status": "success", "message": "تم الأرشفة والتعميد بنجاح"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": f"تعثر في الترسانة: {str(e)}"}), 500

    return render_template('add_supplier.html')

@admin_bp.route('/suppliers')
@login_required
def manage_suppliers():
    try:
        suppliers_list = Vendor.query.all() if Vendor else []
        return render_template('manage_suppliers.html', suppliers=suppliers_list)
    except:
        return render_template('manage_suppliers.html', suppliers=[])

# --- 4. إدارة الجلسات السيادية ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and getattr(current_user, 'role', 'admin') == 'admin':
        return redirect(url_for('admin.admin_dashboard'))
    return handle_admin_login()

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('تم إغلاق الجلسة الآمنة.', 'info')
    return redirect(url_for('admin.login'))
