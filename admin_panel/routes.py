import os
from flask import render_template, request, redirect, url_for, flash, session, current_app, jsonify
from flask_login import login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from core import db 

# استيراد النماذج (Models)
try:
    from core.models.vendor import Vendor
    from core.models.user import User  # افترضنا وجود نموذج المستخدم الأساسي
    # إضافة نموذج طلبات السحب إذا كان متوفراً
    from core.models.vendor import WithdrawRequest 
except ImportError:
    Vendor = None
    User = None
    WithdrawRequest = None

# استيراد مدير الأرشفة السيادي (GitHub Archive)
from .archive_manager import ArchiveManager

from . import admin_bp
from .auth import handle_admin_login

# تهيئة مدير الأرشفة
archiver = ArchiveManager()

# --- 1. بوابة الدخول والخروج ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """تستدعي قالب login.html عبر دالة handle_admin_login"""
    return handle_admin_login()

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash("تم تأمين الخروج من النظام السيادي.", "info")
    return redirect(url_for('admin.login'))

# --- 2. لوحة التحكم الرئيسية ---
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    """عرض إحصائيات النظام الشاملة"""
    suppliers_count = Vendor.query.count() if Vendor else 0
    # يمكن إضافة إحصائيات الأرصدة وطلبات السحب هنا
    return render_template('dashboard.html', suppliers_count=suppliers_count)

# --- 3. إدارة الموردين (التعميد والأرشفة) ---
@admin_bp.route('/add-supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    """
    إدارة عملية التعميد السيادي:
    1. توليد الرقم التسلسلي.
    2. رفع الوثائق إلى الأرشيف الخارجي (GitHub).
    3. إنشاء حساب مستخدم ومورد في القاعدة المحلية.
    """
    # توليد الرقم السيادي التالي (يبدأ من 1001)
    next_id = 1001
    if Vendor:
        last_vendor = Vendor.query.order_by(Vendor.id.desc()).first()
        if last_vendor:
            next_id = last_vendor.id + 1001 # أو حسب منطق التسلسل المفضل لديك

    if request.method == 'POST':
        try:
            # أ- استلام البيانات من النموذج
            username = request.form.get('username')
            password = request.form.get('password', '123')
            e_wallet = request.form.get('e_wallet') # الرقم المولد في الواجهة
            
            # معالجة المدخلات التي قد تكون يدوية (Manual Input)
            activity = request.form.get('manual_activity') if request.form.get('activity_type') == 'manual' else request.form.get('activity_type')
            id_type = request.form.get('manual_id_type') if request.form.get('id_type') == 'manual' else request.form.get('id_type')
            bank_name = request.form.get('manual_bank') if request.form.get('bank_name') == 'other' else request.form.get('bank_name')

            # ب- الأرشفة الخارجية (GitHub)
            id_file = request.files.get('id_image')
            github_path = None
            
            if id_file and id_file.filename:
                ext = os.path.splitext(id_file.filename)[1]
                file_data = id_file.read()
                
                # رفع صورة الهوية للأرشيف الهرمي
                github_path = archiver.upload_document(
                    s_id=e_wallet, 
                    u_id=username, 
                    doc_t="Identity_Doc", 
                    file_d=file_data, 
                    ext=ext
                )
                
                # أرشفة السجل النصي الكامل للمورد (نسخة احتياطية سيادية)
                archiver.upload_full_package(
                    data={
                        'supplier_id': e_wallet,
                        'username': username,
                        'full_name': request.form.get('owner_name'),
                        'province': request.form.get('province'),
                        'district': request.form.get('district'),
                        'bank_name': bank_name,
                        'bank_acc': request.form.get('bank_acc')
                    },
                    files=[] # تم الرفع بالأعلى
                )

            # ج- إنشاء السجلات في قاعدة البيانات المحلية
            # 1. إنشاء المستخدم المرتبط
            new_user = User(
                username=username,
                password=generate_password_hash(password),
                role='vendor'
            )
            db.session.add(new_user)
            db.session.flush() # للحصول على user_id قبل الـ commit النهائي

            # 2. إنشاء بيانات المورد
            new_vendor = Vendor(
                user_id=new_user.id,
                owner_name=request.form.get('owner_name'),
                id_type=id_type,
                id_card_number=request.form.get('id_card_number'),
                id_image_path=github_path, # حفظ مسار GitHub
                trade_name=request.form.get('trade_name'),
                activity_type=activity,
                province=request.form.get('province'),
                district=request.form.get('district'),
                address_detail=request.form.get('address_detail'),
                phone=request.form.get('phone'),
                e_wallet=e_wallet,
                fin_type=request.form.get('fin_type'),
                bank_name=bank_name,
                bank_acc=request.form.get('bank_acc'),
                is_verified=True
            )
            
            db.session.add(new_vendor)
            db.session.commit()

            # إرجاع استجابة نجاح للـ SweetAlert2
            return jsonify({"status": "success", "message": "تم التعميد والأرشفة بنجاح"}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500

    return render_template('add_supplier.html', next_id=next_id)

# --- 4. طلبات السحب ---
@admin_bp.route('/withdraw-requests')
@login_required
def withdraw_requests():
    """إدارة طلبات تحويل الأرباح للموردين"""
    requests_list = WithdrawRequest.query.filter_by(status='pending').all() if WithdrawRequest else []
    return render_template('withdraw_requests.html', requests=requests_list)

# --- 5. إدارة المحافظ السيادية ---
@admin_bp.route('/wallets')
@login_required
def wallets():
    """مراقبة المحافظ المالية لكل الموردين"""
    all_vendors = Vendor.query.all() if Vendor else []
    return render_template('wallets.html', vendors=all_vendors)
