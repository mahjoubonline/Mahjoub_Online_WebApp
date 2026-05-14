import os
from flask import Blueprint, render_template, request, jsonify, current_app
from werkzeug.utils import secure_filename

# استيراد قاعدة البيانات والموديل (تأكد من صحة مسارات الاستيراد في مشروعك)
from apps.models import db  
from models.supplier_db import Supplier
from apps.utils import admin_required 

# تعريف الـ Blueprint مع تحديد مسار مجلد القوالب الداخلي لحل مشكلة TemplateNotFound
add_supplier_bp = Blueprint(
    'add_supplier', 
    __name__, 
    template_folder='templates'  # يقرأ تلقائياً من: apps/add_supplier/templates/
)

# الامتدادات المسموح برفعها للوثائق والهويات
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --- 1. مسار عرض الواجهة واعتماد المورد (GET & POST) ---
@add_supplier_bp.route('/admin/suppliers/add', methods=['GET', 'POST'])
@admin_required
def add_supplier():
    if request.method == 'POST':
        # أ. استلام البيانات الأساسية من واجهة الـ HTML
        unified_id = request.form.get('unified_id')
        username = request.form.get('username')
        password = request.form.get('password')
        
        # ب. معالجة بيانات الهوية (الاختيار التلقائي أو الإدخال اليدوي)
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
        
        # د. بيانات الربط المالي (بنوك / صرافة) وجهات التحويل
        fin_type = request.form.get('fin_type')
        bank_name = request.form.get('bank_name')
        if bank_name == 'manual':
            bank_name = request.form.get('manual_bank_name')
        bank_acc = request.form.get('bank_acc')
        
        # هـ. فئة المورد (جملة / تجزئة / يدوي)
        category = request.form.get('category')
        if category == 'manual':
            category = request.form.get('manual_category')

        # و. معالجة رفع صورة وثيقة الهوية وتأمينها
        file = request.files.get('identity_image')
        filename = None
        if file and allowed_file(file.filename):
            clean_filename = secure_filename(file.filename)
            # دمج المعرف الموحد لمنع تداخل وتشابه أسماء ملفات الصور في السيرفر
            filename = f"{unified_id}_{clean_filename}"
            
            upload_path = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'uploads'), 'suppliers_ids')
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            file.save(os.path.join(upload_path, filename))

        # ز. الفحص المسبق لمنع التكرار قبل الحفظ (حماية لسلامة البيانات من الـ AJAX)
        if Supplier.query.filter_by(username=username).first():
            return jsonify({'success': False, 'message': 'اسم المستخدم مسجل مسبقاً في النظام!'}), 400
        if Supplier.query.filter_by(trade_name=trade_name).first():
            return jsonify({'success': False, 'message': 'الاسم التجاري للمنشأة مسجل بالفعل!'}), 400
        if Supplier.query.filter_by(shop_phone=shop_phone).first():
            return jsonify({'success': False, 'message': 'رقم الهاتف مرتبط بمورد آخر!'}), 400

        try:
            # ح. إنشاء كائن المورد وضخ البيانات فيه
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
            
            # تشفير كلمة المرور عبر ميكانيكية الـ Hash المدمجة بالموديل السيادي
            new_supplier.set_password(password)
            
            db.session.add(new_supplier)
            db.session.commit()
            
            # إرجاع استجابة JSON نجاح (لأن كود الـ JavaScript ينتظرها لفتح الـ Modal)
            return jsonify({
                'success': True,
                'message': 'تم اعتماد وأرشفة المورد بنجاح',
                'unified_id': unified_id
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'فشل الحفظ في قاعدة البيانات: {str(e)}'}), 500

    # ط. معالجة طلب الـ GET (تحميل الصفحة أول مرة وحساب المعرف القادم للمورد الجديد)
    try:
        max_id = db.session.query(db.func.max(Supplier.id)).scalar()
        next_id = (max_id + 1) if max_id else 1
    except Exception:
        next_id = 1
    
    # سيتوجه الفلاسك تلقائياً للـ Template الصحيح بفضل إعداد الـ Blueprint بالأعلى
    return render_template('admin/add_supplier.html', next_id=next_id)


# --- 2. مسار نظام التحقق اللحظي المنفصل عبر الـ AJAX أثناء الكتابة ---
@add_supplier_bp.route('/admin/suppliers/check-duplicate', methods=['GET'])
@admin_required
def check_duplicate():
    check_type = request.args.get('type')
    value = request.args.get('value', '').strip()
    bank_name = request.args.get('bank_name', '').strip()

    if not check_type or not value:
        return jsonify({'exists': False})

    exists = False

    # فحص تواجد الحقول في قاعدة البيانات لمنع الازدواجية الفورية بالواجهة
    if check_type == 'username':
        exists = Supplier.query.filter_by(username=value).first() is not None
    
    elif check_type == 'trade_name':
        exists = Supplier.query.filter_by(trade_name=value).first() is not None

    elif check_type == 'shop_phone':
        exists = Supplier.query.filter_by(shop_phone=value).first() is not None

    elif check_type == 'bank_acc':
        # تحقق ذكي: يمنع تكرار رقم الحساب في نفس البنك/المصرف فقط
        exists = Supplier.query.filter_by(bank_acc=value, bank_name=bank_name).first() is not None

    return jsonify({'exists': exists})
