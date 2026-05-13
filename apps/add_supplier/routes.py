from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
from models.supplier_db import db, Supplier
import os

# 1. تعريف الـ Blueprint
# ملاحظة: تم تغيير الاسم إلى 'admin' ليطابق url_for('admin.add_supplier') المستخدم في القوالب
add_supplier_bp = Blueprint(
    'admin', 
    __name__, 
    template_folder='templates'
)

# 2. المسار السيادي لإضافة الموردين
@add_supplier_bp.route('/supplier/add', methods=['GET', 'POST'])
def add_supplier(): # تم تغيير اسم الدالة ليطابق الاستدعاء في القالب
    # 🛡️ التحقق من صلاحية المؤسس (علي محجوب)
    if not session.get('is_authenticated'):
        return redirect(url_for('auth.login'))

    # --- أولاً: حالة العرض (GET) ---
    if request.method == 'GET':
        try:
            # حساب المعرف القادم لإظهاره في الواجهة السيادية
            last_supplier = Supplier.query.order_by(Supplier.id.desc()).first()
            next_id_count = (last_supplier.id + 1) if last_supplier else 1
            
            return render_template('admin/add_supplier.html', next_id=next_id_count)
        except Exception as e:
            return f"Error loading supplier page: {str(e)}", 500

    # --- ثانياً: حالة الحفظ (POST) ---
    if request.method == 'POST':
        # استقبال البيانات (دعم JSON و Form Data)
        data = request.get_json() if request.is_json else request.form
        
        try:
            # 1. إنشاء كائن المورد الجديد
            new_supplier = Supplier(
                username=data.get('username'),
                password=data.get('password'),
                email=data.get('email'),
                trade_name=data.get('trade_name'),
                owner_name=data.get('owner_name'),
                phone=data.get('phone'),
                activity_type=data.get('activity_type'),
                province=data.get('province'),
                district=data.get('district'),
                address_detail=data.get('address_detail'),
                bank_name=data.get('bank_name'),
                bank_acc=data.get('bank_acc'),
                identity_type=data.get('identity_type')
            )

            # 2. توليد المعرف السيادي (Sovereign ID)
            count = Supplier.query.count() + 1
            new_supplier.sovereign_id = f"SUP-MHA_963{count}"

            # 3. معالجة رفع صورة الهوية (إن وجدت)
            if 'identity_image' in request.files:
                file = request.files['identity_image']
                if file.filename != '':
                    # حفظ الصورة بمسار منظم (يمكنك تعديله حسب نظام الملفات لديك)
                    filename = f"ID_{new_supplier.sovereign_id}_{file.filename}"
                    file.save(os.path.join('static/uploads/suppliers', filename))
                    new_supplier.identity_image = filename

            # 4. الحفظ في قاعدة البيانات
            db.session.add(new_supplier)
            db.session.commit()

            # الاستجابة الذكية (AJAX أو إعادة توجيه)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
                return jsonify({
                    'status': 'success', 
                    'message': f'تم تعميد المورد بنجاح بالرقم السيادي: {new_supplier.sovereign_id}'
                })
            
            flash(f'تم حفظ المورد {new_supplier.trade_name} بنجاح.', 'success')
            return redirect(url_for('admin.dashboard'))

        except Exception as e:
            db.session.rollback()
            error_msg = f"فشلت عملية الأرشفة: {str(e)}"
            if request.is_json:
                return jsonify({'status': 'error', 'message': error_msg}), 500
            
            flash(error_msg, 'danger')
            return redirect(url_for('admin.add_supplier'))
