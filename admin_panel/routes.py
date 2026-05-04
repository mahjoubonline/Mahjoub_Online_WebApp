# admin_panel/routes.py

import os
import random
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import logout_user, login_required, current_user
from sqlalchemy import text
from sqlalchemy.orm import joinedload
from core import db 
from werkzeug.security import generate_password_hash
from . import admin_bp
from .auth import handle_admin_login

# --- 1. استيراد النماذج (مع معالجة تضارب المسميات) ---
try:
    from core.models.user import User
    # نستخدم المسمى الذي يتعرف عليه السيرفر حالياً لتجنب الانهيار
    from core.models.vendor import Vendor, WithdrawRequest
    try:
        from core.models.business import Order
    except ImportError:
        Order = None
except ImportError as e:
    print(f"❗ Import Warning: {e}")
    User = Vendor = WithdrawRequest = Order = None

# --- 2. خدمات الهوية والمحافظ ---
def generate_vendor_wallet():
    return f"W-MAH-{random.randint(100000, 999999)}"

def get_next_sovereign_id():
    """توليد المعرف السيادي MAH-963 لضمان استقرار 'سوقك الذكي'"""
    try:
        db.session.rollback()
        count = db.session.query(Vendor).count() if Vendor else 0
        return f"MAH-963{count + 1}"
    except:
        return f"MAH-963{random.randint(100, 999)}"

# --- 3. مسار الطوارئ (الترميم الهيكلي) ---
@admin_bp.route('/force-repair-now')
@login_required
def force_repair():
    if getattr(current_user, 'role', '') != 'admin':
        return "Unauthorized", 403
    try:
        db.session.rollback() 
        # تحديث الجداول لإضافة الحقول السيادية الجديدة دون حذف البيانات القديمة
        db.session.execute(text("ALTER TABLE vendors ADD COLUMN IF NOT EXISTS supplier_id VARCHAR(50) UNIQUE;"))
        db.session.execute(text("ALTER TABLE vendors ADD COLUMN IF NOT EXISTS e_wallet VARCHAR(100) UNIQUE;"))
        db.session.execute(text("ALTER TABLE vendors ALTER COLUMN password DROP NOT NULL;"))
        db.session.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT 'vendor';"))
        
        db.session.commit()
        session['repair_done'] = True
        flash("تم ترميم هيكل الترسانة وتحديث المعرفات بنجاح", "success")
        return redirect(url_for('admin.admin_dashboard'))
    except Exception as e:
        db.session.rollback()
        return f"Repair Error: {str(e)}"

# --- 4. لوحة التحكم (مركز المراقبة العليا) ---
@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    if getattr(current_user, 'role', '') != 'admin':
        return redirect(url_for('main.index'))
    try:
        stats = {
            'suppliers_count': db.session.query(Vendor).count() if Vendor else 0,
            'pending_withdrawals': db.session.query(WithdrawRequest).filter_by(status='pending').count() if WithdrawRequest else 0,
            'orders_count': db.session.query(Order).count() if Order else 0
        }
        return render_template('dashboard.html', **stats, show_repair=not session.get('repair_done'))
    except Exception:
        return render_template('dashboard.html', suppliers_count=0, pending_withdrawals=0, orders_count=0, show_repair=True)

# --- 5. حوكمة الموردين (التعميد والحفظ في القاعدة) ---
@admin_bp.route('/add-supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    if request.method == 'POST':
        try:
            db.session.rollback()
            username = request.form.get('username')
            password = request.form.get('password')
            
            if User.query.filter_by(username=username).first():
                return jsonify({"status": "error", "message": "اسم المستخدم مسجل مسبقاً"}), 400

            # إنشاء حساب المستخدم
            new_user = User(
                username=username,
                password_hash=generate_password_hash(password),
                role='vendor'
            )
            db.session.add(new_user)
            db.session.flush() 

            # إنشاء بروفايل المورد (Vendor) وحفظه في القاعدة
            new_vendor = Vendor(
                user_id=new_user.id,
                supplier_id=request.form.get('next_id'), # حفظ معرف MAH-963
                trade_name=request.form.get('trade_name'),
                owner_name=request.form.get('owner_name'),
                phone=request.form.get('phone'),
                e_wallet=request.form.get('e_wallet'),
                activity_type=request.form.get('activity_type'),
                province=request.form.get('province'),
                district=request.form.get('district'),
                # تأكد من تصفير الأرصدة عند البداية
                balance_yer=0.0, balance_sar=0.0, balance_usd=0.0
            )
            
            db.session.add(new_vendor)
            db.session.commit()
            return jsonify({"status": "success", "message": "تم تعميد المورد بنجاح وربطه بالهوية السيادية"})
            
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": f"فشل الحفظ: {str(e)}"}), 500

    return render_template('add_supplier.html', 
                           next_id=get_next_sovereign_id(), 
                           next_wallet=generate_vendor_wallet())

# --- 6. الإدارة والمراقبة ---
@admin_bp.route('/suppliers')
@login_required
def manage_suppliers():
    suppliers_list = Vendor.query.all() if Vendor else []
    return render_template('manage_suppliers.html', suppliers=suppliers_list)

@admin_bp.route('/manage-wallets')
@login_required
def manage_wallets():
    suppliers_list = Vendor.query.all() if Vendor else []
    return render_template('wallets.html', suppliers=suppliers_list)

@admin_bp.route('/withdraw-requests')
@login_required
def withdraw_requests():
    requests_list = WithdrawRequest.query.order_by(WithdrawRequest.id.desc()).all() if WithdrawRequest else []
    return render_template('withdraw_requests.html', requests=requests_list)

# --- 7. إدارة الوصول ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and getattr(current_user, 'role', '') == 'admin':
        return redirect(url_for('admin.admin_dashboard'))
    return handle_admin_login()

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("تم تأمين النظام بنجاح", "info")
    return redirect(url_for('admin.login'))
