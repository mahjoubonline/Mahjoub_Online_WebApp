import os
from flask import Blueprint, render_template, request, jsonify, current_app
from datetime import datetime
from werkzeug.utils import secure_filename

# تعريف الـ Blueprint ليعود إلى مجلد القوالب الرئيسي
admin_suppliers = Blueprint(
    'admin_suppliers', 
    __name__,
    template_folder='../../templates'
)

# امتدادات الملفات المسموحة لرفع الصور
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --- 1. مسار عرض الواجهة واعتماد المورد ---
@admin_suppliers.route('/admin/suppliers/add', methods=['GET', 'POST'])
def add_supplier():
    # استيراد محلي لتجنب التعارض الدائري
    from models.supplier_db import db, Supplier 

    if request.method == 'POST':
        try:
            unified_id = request.form.get('unified_id')
            username = request.form.get('username')
            password = request.form.get('password')
            
            category = request.form.get('category')
            if category == 'manual':
                category = request.form.get('manual_category')

            owner_name = request.form.get('owner_name')
            trade_name = request.form.get('trade_name')
            shop_phone = request.form.get('shop_phone')
            
            province = request.form.get('province')
            district = request.form.get('district')
            address_detail = request.form.get('address') 

            fin_type = request.form.get('fin_type')
            bank_name = request.form.get('bank_name')
            if bank_name == 'manual':
                bank_name = request.form.get('manual_bank_name')
            bank_acc = request.form.get('bank_acc')

            # فحص التكرار بأمان داخل بيئة الـ POST
            if Supplier.query.filter_by(username=username).first():
                return jsonify({'status': 'error', 'message': 'اسم المستخدم مسجل مسبقاً!'}), 400
            if Supplier.query.filter_by(trade_name=trade_name).first():
                return jsonify({'status': 'error', 'message': 'الاسم التجاري مسجل مسبقاً!'}), 400

            # بناء السجل
            new_supplier = Supplier(
                sovereign_id=unified_id,
                username=username,
                password=password, 
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
                created_at=datetime.utcnow()
            )

            db.session.add(new_supplier)
            db.session.commit()

            return jsonify({
                'status': 'success',
                'data': {
                    'sovereign_id': unified_id,
                    'username': username,
                    'password': password
                }
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'message': f'حدث خطأ في النظام: {str(e)}'
            }), 500

    # === حماية طلب الـ GET لمنع خطأ 500 نهائياً ===
    next_id_num = 1
    try:
        # محاولة جلب آخر معرف من قاعدة البيانات
        last_supplier = Supplier.query.order_by(Supplier.id.desc()).first()
        if last_supplier:
            next_id_num = last_supplier.id + 1
    except Exception as db_error:
        # إذا فشل الاتصال أو حدث خطأ في سياق الـ db، لا تجعل السيرفر ينهار
        print(f"Database context warning (Using default ID 1): {str(db_error)}")
        next_id_num = 1
        
    # نقوم بإرسال المتغير بكلا الاسمين (next_id و next_id_num) لضمان توافقه مع ملف الـ HTML الخاص بك أياً كان المسمى المدون فيه
    return render_template('admin/add_supplier.html', next_id=next_id_num, next_id_num=next_id_num)


# --- 2. مسار التحقق اللحظي عبر الـ AJAX ---
@admin_suppliers.route('/admin/suppliers/check-duplicate', methods=['GET'])
def check_duplicate():
    from models.supplier_db import Supplier 

    check_type = request.args.get('type')
    value = request.args.get('value', '').strip()
    bank_name = request.args.get('bank_name', '').strip()

    if not check_type or not value:
        return jsonify({'exists': False})

    exists = False
    try:
        if check_type == 'username':
            exists = Supplier.query.filter_by(username=value).first() is not None
        elif check_type == 'trade_name':
            exists = Supplier.query.filter_by(trade_name=value).first() is not None
        elif check_type == 'shop_phone':
            exists = Supplier.query.filter_by(shop_phone=value).first() is not None
        elif check_type == 'bank_acc':
            exists = Supplier.query.filter_by(bank_account=value, bank_name=bank_name).first() is not None
    except Exception:
        exists = False

    return jsonify({'exists': exists})
