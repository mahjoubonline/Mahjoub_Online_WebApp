# coding: utf-8
import os
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from datetime import datetime
from werkzeug.security import generate_password_hash

# 🚀 استيراد قاعدة البيانات والموديل بمسارات مطلقة
from apps import db  
from apps.models.supplier_db import Supplier 

current_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_dir, 'templates')

admin_suppliers = Blueprint(
    'admin_suppliers', 
    __name__,
    template_folder=template_path
)

@admin_suppliers.route('/add', methods=['GET', 'POST'])
@login_required 
def add_supplier():
    if request.method == 'POST':
        try:
            # 1. استقبال البيانات الأساسية
            username = request.form.get('username', '').strip()
            trade_name = request.form.get('trade_name', '').strip()
            password = request.form.get('password')

            # 2. التحقق النهائي (حماية إضافية للباكيند)
            if Supplier.query.filter_by(username=username).first():
                return jsonify({'status': 'error', 'message': 'اسم المستخدم مسجل مسبقاً!'}), 400

            # 3. معالجة حقول الإدخال اليدوي الديناميكية
            
            # أ) نوع الهوية
            identity_type = request.form.get('identity_type')
            if identity_type == 'manual':
                identity_type = request.form.get('manual_identity_type', '').strip()

            # ب) جهة التحويل المالي
            bank_name = request.form.get('bank_name')
            if bank_name == 'manual':
                bank_name = request.form.get('manual_bank_name', '').strip()

            # ج) فئة المورد (الاحتفاظ بالقيمة الجديدة)
            # نأخذ القيمة من select أولاً، وإذا كانت manual نأخذها من حقل التحديث اللحظي
            category = request.form.get('category', '').strip()
            # في حال كان التصميم يرسل القيمة اليدوية في حقل منفصل عند اختيار 'manual'
            if category == 'manual':
                 category = request.form.get('manual_category_input', '').strip()

            # 4. تشفير كلمة المرور وإنشاء الكائن
            hashed_pw = generate_password_hash(password)
            
            new_supplier = Supplier(
                sovereign_id=request.form.get('unified_id'),
                username=username,
                password_hash=hashed_pw,
                identity_type=identity_type,
                identity_number=request.form.get('identity_number', '').strip(),
                activity_type=category,       # هنا يتم حفظ الفئة الجديدة (تحديث لحظي)
                owner_name=request.form.get('owner_name', '').strip(),
                trade_name=trade_name,
                shop_phone=request.form.get('shop_phone', '').strip(),
                province=request.form.get('province'),
                district=request.form.get('district'),
                address_detail=request.form.get('address'),
                fin_type=request.form.get('fin_type'),
                bank_name=bank_name,
                bank_acc=request.form.get('bank_acc', '').strip(),
                created_at=datetime.utcnow()
            )

            # 5. معالجة الصورة (اختياري)
            if 'identity_image' in request.files:
                file = request.files['identity_image']
                if file and file.filename != '':
                    # منطق حفظ الملف يوضع هنا
                    pass

            # 6. الاعتماد النهائي في القاعدة
            db.session.add(new_supplier)
            db.session.commit()

            return jsonify({
                'status': 'success',
                'message': 'تم تسجيل وتعميد المورد بنجاح'
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': f'خطأ تقني: {str(e)}'}), 500

    # حساب الـ ID التالي للعرض
    try:
        last_s = Supplier.query.order_by(Supplier.id.desc()).first()
        next_id = (last_s.id + 1) if last_s else 1
    except:
        next_id = 1
    
    return render_template('admin/add_supplier.html', next_id=next_id)

# محرك التحقق اللحظي من البيانات (API)
@admin_suppliers.route('/check-duplicate', methods=['GET'])
@login_required
def check_duplicate():
    check_type = request.args.get('type')
    value = request.args.get('value', '').strip()

    if not check_type or not value:
        return jsonify({'exists': False})

    # خريطة الحقول للتحقق الديناميكي
    field_map = {
        'username': Supplier.username,
        'trade_name': Supplier.trade_name,
        'shop_phone': Supplier.shop_phone
    }

    target_field = field_map.get(check_type)
    exists = False
    
    if target_field:
        exists = Supplier.query.filter(target_field == value).first() is not None

    return jsonify({'exists': exists})
