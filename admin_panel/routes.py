import os
import re
import random
import string
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import text
from core import db 
from werkzeug.security import generate_password_hash

# --- 1. استيراد النماذج مع تصحيح المسارات ---
try:
    from core.models.user import User
    from core.models.vendor import Vendor, WithdrawRequest
    # استيراد النماذج من الترسانة الرقمية
    try:
        from core.models.business import Order, Supplier
    except ImportError:
        Order = Supplier = None
except ImportError as e:
    print(f"❗ Import Warning: {e}")
    User = Vendor = WithdrawRequest = None

# --- 2. خدمات المحافظ ---
def generate_vendor_wallet():
    # توليد محفظة فريدة تتبع نمط محجوب أونلاين
    return f"W-MAH-{random.randint(100000, 999999)}"

from . import admin_bp
from .auth import handle_admin_login

def get_next_sovereign_id():
    try:
        db.session.rollback()
        count = db.session.query(Vendor).count() if Vendor else 0
        return f"MAH-963{count + 1}"
    except:
        return f"MAH-963{random.randint(100, 999)}"

# --- 3. مسار الطوارئ (تحديث الهيكل) ---
@admin_bp.route('/force-repair-now')
def force_repair():
    try:
        db.session.rollback() 
        db.session.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT 'admin';"))
        db.create_all()
        db.session.commit()
        session['repair_done'] = True
        flash("تم تحديث هيكل النظام بنجاح", "success")
        return redirect(url_for('admin.admin_dashboard'))
    except Exception as e:
        db.session.rollback()
        return f"Repair Error: {str(e)}"

# --- 4. لوحة التحكم ---
@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    try:
        stats = {
            'suppliers_count': db.session.query(Vendor).count() if Vendor else 0,
            'pending_withdrawals': db.session.query(WithdrawRequest).filter_by(status='pending').count() if WithdrawRequest else 0
        }
        return render_template('dashboard.html', **stats, show_repair=not session.get('repair_done'))
    except Exception as e:
        db.session.rollback()
        return render_template('dashboard.html', suppliers_count=0, pending_withdrawals=0, show_repair=True)

# --- 5. حوكمة الموردين (التعميد السيادي) ---
@admin_bp.route('/add-supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    if request.method == 'POST':
        try:
            db.session.rollback()
            
            # أ - إنشاء المستخدم الأساسي للدخول للنظام
            username = request.form.get('username')
            password = request.form.get('password')
            
            if User.query.filter_by(username=username).first():
                return jsonify({"status": "error", "message": "اسم المستخدم موجود مسبقاً"}), 400

            new_user = User(
                username=username,
                password=generate_password_hash(password),
                role='vendor'
            )
            db.session.add(new_user)
            db.session.flush() # للحصول على ID المستخدم الجديد

            # ب - استخراج البيانات الجغرافية والنشاط
            activity = request.form.get('activity_type')
            if activity == 'manual': activity = request.form.get('manual_activity')
            
            id_type = request.form.get('id_type')
            if id_type == 'manual': id_type = request.form.get('manual_id_type')

            # ج - إنشاء ملف المورد (Vendor Profile) في الترسانة
            new_vendor = Vendor(
                user_id=new_user.id,
                supplier_id=request.form.get('next_id'),
                trade_name=request.form.get('trade_name'),
                owner_name=request.form.get('owner_name'),
                phone=request.form.get('phone'),
                e_wallet=request.form.get('e_wallet'),
                activity_type=activity,
                id_type=id_type,
                id_card_number=request.form.get('id_card_number'),
                province=request.form.get('province'),
                district=request.form.get('district'),
                address_detail=request.form.get('address_detail'),
                bank_name=request.form.get('bank_name') if request.form.get('bank_name') != 'other' else request.form.get('manual_bank'),
                bank_acc=request.form.get('bank_acc'),
                fin_type=request.form.get('fin_type')
            )
            
            db.session.add(new_vendor)
            db.session.commit()
            
            return jsonify({"status": "success", "message": "تم تعميد المورد وربط المحفظة بنجاح"})

        except Exception as e:
            db.session.rollback()
            print(f"❌ Error in add_supplier: {str(e)}")
            return jsonify({"status": "error", "message": str(e)}), 500

    # في حالة الـ GET: تجهيز المعرفات والبيانات
    return render_template('add_supplier.html', 
                           next_id=get_next_sovereign_id(),
                           next_wallet=generate_vendor_wallet())

# --- 6. إدارة المحافظ والموردين ---
@admin_bp.route('/suppliers')
@login_required
def manage_suppliers():
    suppliers_list = Vendor.query.all() if Vendor else []
    return render_template('manage_suppliers.html', suppliers=suppliers_list)

@admin_bp.route('/manage-wallets')
@login_required
def manage_wallets():
    suppliers_list = Vendor.query.all() if Vendor else []
    return render_template('manage_wallets.html', suppliers=suppliers_list)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and getattr(current_user, 'role', 'admin') == 'admin':
        return redirect(url_for('admin.admin_dashboard'))
    return handle_admin_login()
