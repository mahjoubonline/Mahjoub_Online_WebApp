import os
from flask import Blueprint, render_template, request, jsonify, current_app
from datetime import datetime
from werkzeug.utils import secure_filename
from .models import db, Supplier  # افترضت وجود موديل باسم Supplier

admin_suppliers = Blueprint('admin_suppliers', __name__)

@admin_suppliers.route('/admin/suppliers/add', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        try:
            # 1. استخراج البيانات الأساسية من النموذج
            unified_id = request.form.get('unified_id')
            username = request.form.get('username')
            password = request.form.get('password')
            
            # معالجة الفئة (إذا كانت "أخرى" نأخذ القيمة اليدوية)
            category = request.form.get('category')
            if category == 'manual':
                category = request.form.get('manual_category')

            owner_name = request.form.get('owner_name')
            trade_name = request.form.get('trade_name')
            shop_phone = request.form.get('shop_phone')
            
            province = request.form.get('province')
            district = request.form.get('district')
            address_detail = request.form.get('address_detail')
            
            fin_type = request.form.get('fin_type')
            bank_name = request.form.get('bank_name')
            bank_acc = request.form.get('bank_acc')

            # 2. التحقق من تكرار البيانات الحساسة (إضافي للأمان)
            if Supplier.query.filter_by(username=username).first():
                return jsonify({'status': 'error', 'message': 'اسم المستخدم مسجل مسبقاً'}), 400

            # 3. معالجة رفع صورة الهوية (اختياري)
            identity_image = request.files.get('identity_image')
            image_filename = None
            if identity_image and identity_image.filename != '':
                filename = secure_filename(f"{unified_id}_{identity_image.filename}")
                # تأكد من إنشاء مجلد الرفع في إعدادات التطبيق
                # identity_image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                image_filename = filename

            # 4. حفظ المورد في قاعدة البيانات
            new_supplier = Supplier(
                sovereign_id=unified_id,
                username=username,
                password=password,  # يفضل استخدام hash_password في بيئة الإنتاج
                category=category,
                owner_name=owner_name,
                trade_name=trade_name,
                shop_phone=shop_phone,
                province=province,
                district=district,
                address_detail=address_detail,
                finance_type=fin_type,
                bank_name=bank_name,
                bank_account=bank_acc,
                identity_image=image_filename,
                registration_date=datetime.now()
            )

            db.session.add(new_supplier)
            db.session.commit()

            # 5. إرجاع استجابة النجاح لتظهر في الـ Modal
            return jsonify({
                'status': 'success',
                'data': {
                    'sovereign_id': unified_id,
                    'username': username,
                    'password': password
                }
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'error', 
                'message': f'حدث خطأ أثناء الحفظ: {str(e)}'
            }), 500

    # في حالة GET: حساب المعرف التالي للعرض في الصفحة
    # التنسيق المطلوب: SUP-WEL-MAH963 + الرقم التسلسلي
    last_supplier = Supplier.query.order_by(Supplier.id.desc()).first()
    next_id_num = (last_supplier.id + 1) if last_supplier else 1
    
    return render_template('admin/add_supplier.html', next_id=next_id_num)

# مسار إضافي للفحص اللحظي (إذا أردت تفعيله في الواجهة مستقبلاً)
@admin_suppliers.route('/admin/suppliers/check-exists', methods=['GET'])
def check_exists():
    username = request.args.get('username')
    exists = Supplier.query.filter_by(username=username).first() is not None
    return jsonify({'exists': exists})
