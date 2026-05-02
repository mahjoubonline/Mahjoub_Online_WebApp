import os
from flask import render_template, request, redirect, url_for, flash, session, current_app, jsonify
from flask_login import login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from core import db 

# --- استيراد النماذج (Models) ---
from core.models.vendor import Vendor
from core.models.user import User 

try:
    from core.models.vendor import WithdrawRequest 
except ImportError:
    WithdrawRequest = None

try:
    from .archive_manager import ArchiveManager
    archiver = ArchiveManager()
except (ImportError, Exception):
    archiver = None

from . import admin_bp
from .auth import handle_admin_login

# --- 1. بوابة الدخول والخروج ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    # إذا كان المستخدم مسجلاً دخوله بالفعل، وجهه مباشرة للداشبورد
    if current_user.is_authenticated:
        return redirect(url_for('admin.admin_dashboard'))
    return handle_admin_login()

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash("تم تأمين الخروج من النظام السيادي.", "info")
    return redirect(url_for('admin.login'))

# --- 2. لوحة التحكم الرئيسية (الداشبورد) ---
@admin_bp.route('/') # مسار الجذر
@admin_bp.route('/dashboard')
@login_required # حماية سيادية
def admin_dashboard():
    # تنظيف الجلسة لتجاوز أي أخطاء SQL سابقة عالقة
    db.session.rollback()
    
    try:
        # حساب الإحصائيات
        suppliers_count = Vendor.query.count()
        pending_withdrawals = WithdrawRequest.query.filter_by(status='pending').count() if WithdrawRequest else 0
        
        return render_template('dashboard.html', 
                               suppliers_count=suppliers_count, 
                               pending_withdrawals=pending_withdrawals)
    except Exception as e:
        # في حال حدوث خطأ في القاعدة، لا ينهار النظام بل يعرض أصفاراً
        print(f"⚠️ Dashboard Error: {str(e)}")
        db.session.rollback()
        return render_template('dashboard.html', suppliers_count=0, pending_withdrawals=0)

# --- 3. إدارة الموردين (التعميد والأرشفة) ---
@admin_bp.route('/add-supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    # توليد المعرف السيادي التالي
    next_id = "MAH-9631"
    try:
        db.session.rollback()
        last_vendor = Vendor.query.order_by(Vendor.id.desc()).first()
        if last_vendor and last_vendor.e_wallet and '-' in last_vendor.e_wallet:
            current_num = int(last_vendor.e_wallet.split('-')[1])
            next_id = f"MAH-{current_num + 1}"
    except:
        next_id = "MAH-9631"

    if request.method == 'POST':
        db.session.rollback()
        try:
            username = request.form.get('username')
            password = request.form.get('password', '123')
            e_wallet = request.form.get('e_wallet') or next_id
            
            if User.query.filter_by(username=username).first():
                return jsonify({"status": "error", "message": "اسم المستخدم مسجل مسبقاً"}), 400

            # الأرشفة السيادية
            github_path = "Local_Archive_Only"
            id_file = request.files.get('id_image')
            if archiver and id_file and id_file.filename:
                github_path = archiver.upload_document(e_wallet, username, "Identity_Doc", id_file.read(), os.path.splitext(id_file.filename)[1])

            # إنشاء المستخدم والمورد في عملية واحدة (Transaction)
            new_user = User(
                username=username,
                password_hash=generate_password_hash(password),
                role='vendor',
                is_active_account=True
            )
            db.session.add(new_user)
            db.session.flush() 

            new_vendor = Vendor(
                user_id=new_user.id,
                owner_name=request.form.get('owner_name'),
                id_type=request.form.get('id_type'),
                id_card_number=request.form.get('id_card_number'),
                id_image_path=github_path,
                trade_name=request.form.get('trade_name'),
                activity_type=request.form.get('manual_activity') if request.form.get('activity_type') == 'manual' else request.form.get('activity_type'),
                province=request.form.get('province'),
                district=request.form.get('district'),
                address_detail=request.form.get('address_detail'),
                phone=request.form.get('phone'),
                e_wallet=e_wallet,
                fin_type=request.form.get('fin_type'),
                bank_name=request.form.get('bank_name'),
                bank_acc=request.form.get('bank_acc'),
                is_verified=True
            )
            db.session.add(new_vendor)
            db.session.commit()
            return jsonify({"status": "success", "message": "تم التعميد بنجاح"}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": f"خطأ في العملية: {str(e)}"}), 500

    return render_template('add_supplier.html', next_id=next_id)

# --- 4. المحافظ وطلبات السحب ---
@admin_bp.route('/withdraw-requests')
@login_required
def withdraw_requests():
    db.session.rollback()
    requests_list = WithdrawRequest.query.filter_by(status='pending').all() if WithdrawRequest else []
    return render_template('withdraw_requests.html', requests=requests_list)

@admin_bp.route('/wallets')
@login_required
def wallets():
    db.session.rollback()
    all_vendors = Vendor.query.all()
    return render_template('wallets.html', vendors=all_vendors)
