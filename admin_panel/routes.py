import os
from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, logout_user
from werkzeug.utils import secure_filename
from core import db 

# استيراد النماذج من قلب النظام (core)
try:
    from core.models import Vendor, User
    from core.models.vendor import WithdrawRequest
except ImportError:
    # لتجنب توقف النظام في حال لم يتم تعريف الموديلات بعد
    WithdrawRequest = None
    Vendor = None
    User = None

from . import admin_bp
from .auth import handle_admin_login

# مسار تخزين الوثائق السيادية
UPLOAD_FOLDER = 'static/uploads/ids'

@admin_bp.route('/add-supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    """
    إضافة مورد جديد لشبكة محجوب أونلاين.
    يتم هنا الربط بين واجهة HTML، موديل الـ Vendor، وعملية رفع الملفات.
    """
    
    # حساب الرقم السيادي القادم (ID) لعرضه في الواجهة
    next_id = 1001
    if Vendor:
        last_vendor = Vendor.query.order_by(Vendor.id.desc()).first()
        if last_vendor:
            next_id = last_vendor.id + 1

    if request.method == 'POST':
        # معالجة رفع الصورة (ID Image)
        id_image = request.files.get('id_image')
        id_image_path = None
        
        if id_image and id_image.filename != '':
            filename = secure_filename(f"id_{request.form.get('username')}_{id_image.filename}")
            target_dir = os.path.join(current_app.root_path, UPLOAD_FOLDER)
            
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            
            id_image.save(os.path.join(target_dir, filename))
            id_image_path = f"{UPLOAD_FOLDER}/{filename}"

        try:
            # 1. إنشاء حساب المستخدم (User)
            new_user = User(username=request.form.get('username'), role='vendor')
            new_user.set_password(request.form.get('password'))
            db.session.add(new_user)
            db.session.flush() 

            # 2. إنشاء سجل المورد (Vendor) وربطه بالرقم السيادي
            new_vendor = Vendor(
                user_id=new_user.id,
                owner_name=request.form.get('owner_name'),
                id_type=request.form.get('id_type'),
                id_card_number=request.form.get('id_card_number'),
                id_image_path=id_image_path, # حفظ مسار الوثيقة المرفوعة
                trade_name=request.form.get('trade_name'),
                activity_type=request.form.get('activity_type'),
                province=request.form.get('province'),
                district=request.form.get('district'),
                address_detail=request.form.get('address_detail'),
                phone=request.form.get('phone'),
                e_wallet=str(next_id), # المحفظة السيادية الموحدة
                bank_name=request.form.get('bank_name'),
                bank_acc=request.form.get('bank_acc')
            )
            
            db.session.add(new_vendor)
            db.session.commit()
            
            flash(f"تم تعميد المورد بنجاح. الرقم الموحد: {next_id}", "success")
            return redirect(url_for('admin.admin_dashboard'))

        except Exception as e:
            db.session.rollback()
            flash(f"خلل في حفظ البيانات: {str(e)}", "danger")

    return render_template('add_supplier.html', next_id=next_id)

# استدعاء بقية الوظائف (Dashboard, Login, Logout)
# ... (تستمر الدوال كما هي في الملف السابق)
