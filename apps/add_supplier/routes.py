import os
from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
from apps import db  
from models.supplier_db import Supplier 

# حساب المسار الديناميكي المشترك للمجلد الرئيسي 'templates' لضمان قراءة الأب والابن معاً
current_dir = os.path.dirname(os.path.abspath(__file__))
global_template_dir = os.path.abspath(os.path.join(current_dir, '..', 'templates'))

admin_suppliers = Blueprint(
    'admin_suppliers', 
    __name__,
    template_folder=global_template_dir
)

@admin_suppliers.route('/add', methods=['GET', 'POST'])
def add_supplier():
    # الأمان السيادي: فحص وإنشاء الجدول فوراً عند طلب الصفحة
    try:
        db.create_all()
    except Exception as e:
        print(f"⚠️ DB create failed or exists: {e}")

    if request.method == 'POST':
        try:
            # استقبال البيانات المرسلة من الفرونت إند عبر AJAX
            unified_id = request.form.get('unified_id')
            username = request.form.get('username', '').strip()
            password = request.form.get('password')
            
            category = request.form.get('category')
            business_type = request.form.get('business_type')  # 🌟 الحقل الجديد المستلم
            owner_name = request.form.get('owner_name', '').strip()
            trade_name = request.form.get('trade_name', '').strip()
            shop_phone = request.form.get('shop_phone', '').strip()
            
            province = request.form.get('province')
            district = request.form.get('district')
            address_detail = request.form.get('address') 

            fin_type = request.form.get('fin_type')
            bank_name = request.form.get('bank_name')
            if bank_name == 'manual':
                bank_name = request.form.get('manual_bank_name')
            bank_acc = request.form.get('bank_acc', '').strip()

            # جدار الحماية النهائي: التحقق الأخير في الباك إند لمنع التكرار الشديد
            if Supplier.query.filter_by(username=username).first():
                return jsonify({'status': 'error', 'message': 'عذراً، اسم المستخدم مسجل مسبقاً!'}), 400
            if Supplier.query.filter_by(trade_name=trade_name).first():
                return jsonify({'status': 'error', 'message': 'عذراً، الاسم التجاري للمنشأة مسجل مسبقاً!'}), 400

            # إنشاء وتجهيز كائن المورد الجديد لحفظه
            # (تأكد أن موديل Supplier في ملف supplier_db.py يحتوي على أعمدة متوافقة مع هذه المتغيرات، مثل business_type إذا أردت حفظه)
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

            # إذا كان العمود متوفراً في الموديل كـ business_type يمكنك تفعيله هنا:
            if hasattr(Supplier, 'business_type'):
                new_supplier.business_type = business_type

            db.session.add(new_supplier)
            db.session.commit()

            return jsonify({
                'status': 'success',
                'data': {
                    'username': username,
                    'password': password
                }
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': f'حدث خطأ في الخادم: {str(e)}'}), 500

    # احتساب الرقم التسلسلي القادم تلقائياً للواجهة
    next_id_num = 1
    try:
        last_supplier = Supplier.query.order_by(Supplier.id.desc()).first()
        if last_supplier:
            next_id_num = last_supplier.id + 1
    except Exception:
        next_id_num = 1
        
    return render_template('admin/add_supplier.html', next_id=next_id_num, next_id_num=next_id_num)


@admin_suppliers.route('/check-duplicate', methods=['GET'])
def check_duplicate():
    """ 🌟 محرك الفحص اللحظي الفيدرالي المحدث """
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
        elif check_type == 'owner_name':
            exists = Supplier.query.filter_by(owner_name=value).first() is not None
        elif check_type == 'shop_phone':
            exists = Supplier.query.filter_by(shop_phone=value).first() is not None
        elif check_type == 'bank_acc':
            # التحقق من عدم تكرار نفس رقم الحساب لنفس جهة الصرافة أو البنك
            exists = Supplier.query.filter_by(bank_account=value, bank_name=bank_name).first() is not None
    except Exception as e:
        print(f"Validation endpoint query error: {e}")
        exists = False

    return jsonify({'exists': exists})
