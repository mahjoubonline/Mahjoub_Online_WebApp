import os
from flask import Blueprint, render_template, request, jsonify, current_app
from werkzeug.utils import secure_filename

# استيراد قاعدة البيانات والكائنات السيادية للنظام
from apps.models import db  
from models.supplier_db import Supplier
from apps.utils import admin_required 

# تعريف الـ Blueprint للمحرك
add_supplier_bp = Blueprint('add_supplier', __name__)

# صيغ ملفات الهوية المسموح برفعها في النظام
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- 1. مسار عرض الواجهة واعتماد المورد ---
@add_supplier_bp.route('/admin/suppliers/add', methods=['GET', 'POST'])
@admin_required
def add_supplier():
    if request.method == 'POST':
        # أ. استلام البيانات الأساسية من النموذج
        unified_id = request.form.get('unified_id')
        username = request.form.get('username')
        password = request.form.get('password')
        
        # ب. معالجة بيانات الهوية والتوثيق (القائمة أو الإدخال اليدوي)
        identity_type = request.form.get('identity_type')
        if identity_type == 'manual':
            identity_type = request.form.get('manual_identity_type')
        identity_number = request.form.get('identity_number')
        
        # ج. بيانات المالك والمنشأة والنطاق الجغرافي
        owner_name = request.form.get('owner_name')
        trade_name = request.form.get('trade_name')
        shop_phone = request.form.get('shop_phone')
        province = request.form.get('province')
        district = request.form.get('district')
        address = request.form.get('address')
        
        # د. الربط المالي (بنوك / صرافة) وجهة التحويل الحالية
        fin_type = request.form.get('fin_type')
        bank_name = request.form.get('bank_name')
        if bank_name == 'manual':
            bank_name = request.form.get('manual_bank_name')
        bank_acc = request.form.get('bank_acc')
        
        # هـ. فئة المورد (جملة / تجزئة)
        category = request.form.get('category')
        if category == 'manual':
            category = request.form.get('manual_category')

        # و. معالجة رفع وحفظ صورة الوثيقة سيادياً
        file = request.files.get('identity_image')
        filename = None
        if file and allowed_file(file.filename):
            clean_filename = secure_filename(file.filename)
            # دمج المعرف الموحد مع اسم الملف لمنع تداخل الصور
            filename = f"{unified_id}_{clean_filename}"
            
            upload_path = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'uploads'), 'suppliers_ids')
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            file.save(os.path.join(upload_path, filename))

        # ز. الفحص الأمني المسبق لمنع التكرار قبل محاولة الحفظ في قاعدة البيانات
        if Supplier.query.filter_by(username=username).first():
            return jsonify({'success': False, 'message': 'اسم المستخدم مسجل مسبقاً في النظام!'}), 400
        if Supplier.query.filter_by(trade_name=trade_name).first():
            return jsonify({'success': False, 'message': 'الاسم التجاري للمنشأة مسجل بالفعل!'}), 400
        if Supplier.query.filter_by(shop_phone=shop_phone).first():
            return jsonify({'success': False, 'message': 'رقم الهاتف مرتبط بمورد آخر!'}), 400

        try:
            # ح. بناء كائن المورد الجديد وتخزينه
            new_supplier = Supplier(
                unified_id=unified_id,
                username=username,
                identity_type=identity_type,
                identity_number=identity_number,
                identity_image=filename,
                owner_name=owner_name,
                trade_name=trade_name,
                shop_phone=shop_phone,
                province=province,
                district=district,
                address=address,
                fin_type=fin_type,
                bank_name=bank_name,
                bank_acc=bank_acc,
                category=category
            )
            
            # تشفير كلمة المرور عبر ميكانيكية الـ Hash المدمجة بالموديل
            new_supplier.set_password(password)
            
            db.session.add(new_supplier)
            db.session.commit()
            
            # إرجاع استجابة JSON نجاح متوافقة مع الـ AJAX الخاص بك لتفعيل الـ Modal
            return jsonify({
                'success': True,
                'message': 'تم اعتماد وأرشفة المورد بنجاح',
                'unified_id': unified_id
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'فشل الحفظ في قاعدة البيانات: {str(e)}'}), 500

    # ط. معالجة طلب الـ GET (حساب المعرف القادم للمورد الجديد وعرض الصفحة)
    try:
        max_id = db.session.query(db.func.max(Supplier.id)).scalar()
        next_id = (max_id + 1) if max_id else 1
    except Exception:
        next_id = 1
    
    return render_template('admin/add_supplier.html', next_id=next_id)


# --- 2. مسار نظام التحقق اللحظي والمنفصل عبر الـ AJAX ---
@add_supplier_bp.route('/admin/suppliers/check-duplicate', methods=['GET'])
@admin_required
def check_duplicate():
    check_type = request.args.get('type')
    value = request.args.get('value', '').strip()
    bank_name = request.args.get('bank_name', '').strip()

    if not check_type or not value:
        return jsonify({'exists': False})

    exists = False

    # فحص الحقول المدخلة لمنع الازدواجية فوراً أثناء الكتابة في الواجهة
    if check_type == 'username':
        exists = Supplier.query.filter_by(username=value).first() is not None
    
    elif check_type == 'trade_name':
        exists = Supplier.query.filter_by(trade_name=value).first() is not None

    elif check_type == 'shop_phone':
        exists = Supplier.query.filter_by(shop_phone=value).first() is not None

    elif check_type == 'bank_acc':
        # التحقق المشترك لضمان عدم تكرار رقم الحساب في نفس البنك/المصرف فقط
        exists = Supplier.query.filter_by(bank_acc=value, bank_name=bank_name).first() is not None

    return jsonify({'exists': exists})
