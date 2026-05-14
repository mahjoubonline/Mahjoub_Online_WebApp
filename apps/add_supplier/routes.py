import os
from flask import Blueprint, render_template, request, jsonify, current_app
from datetime import datetime
from werkzeug.utils import secure_filename

# استيراد قاعدة البيانات والموديل من المسار المحدد في هيكل المشروع
from models.supplier_db import db, Supplier 

# تعريف الـ Blueprint مع توجيه المسار لمجلد القوالب الرئيسي لحل مشكلة الصورة image_955a54.png
admin_suppliers = Blueprint(
    'admin_suppliers', 
    __name__,
    template_folder='../../templates' 
)

@admin_suppliers.route('/admin/suppliers/add', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        try:
            # 1. استلام البيانات الأساسية من واجهة التعميد
            unified_id = request.form.get('unified_id')
            username = request.form.get('username')
            password = request.form.get('password')
            
            # معالجة فئة المورد (ديناميكياً)
            category = request.form.get('category')
            if category == 'manual':
                category = request.form.get('manual_category')

            # 2. بيانات المالك والنشاط التجاري
            owner_name = request.form.get('owner_name')
            trade_name = request.form.get('trade_name')
            shop_phone = request.form.get('shop_phone')
            
            # 3. بيانات العنوان التفصيلية
            province = request.form.get('province')
            district = request.form.get('district')
            address_detail = request.form.get('address_detail')

            # 4. بيانات الربط المالي السيادي
            fin_type = request.form.get('fin_type')
            bank_name = request.form.get('bank_name')
            bank_acc = request.form.get('bank_acc')

            # 5. التحقق من عدم تكرار اسم المستخدم في قاعدة البيانات
            if Supplier.query.filter_by(username=username).first():
                return jsonify({'status': 'error', 'message': 'اسم المستخدم هذا مسجل مسبقاً في النظام'}), 400

            # 6. إنشاء سجل المورد الجديد في المحرك
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

            # إرجاع استجابة النجاح المتوافقة مع الـ Modal في واجهة المستخدم
            return jsonify({
                'status': 'success',
                'data': {
                    'sovereign_id': unified_id,
                    'username': username,
                    'password': password
                }
            })

        except Exception as e:
            # التراجع عن التغييرات في حالة حدوث خطأ تقني لضمان سلامة البيانات
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'message': f'فشل في عملية الحفظ: {str(e)}'
            }), 500

    # في حالة GET: حساب المعرف التسلسلي التالي للموردين
    try:
        last_supplier = Supplier.query.order_by(Supplier.id.desc()).first()
        next_id_num = (last_supplier.id + 1) if last_supplier else 1
    except:
        next_id_num = 1
        
    return render_template('admin/add_supplier.html', next_id=next_id_num)

@admin_suppliers.route('/admin/suppliers/check-duplicate/', methods=['GET'])
def check_duplicate():
    """محرك التحقق اللحظي لضمان عدم تكرار البيانات الحساسة"""
    field_type = request.args.get('type')
    value = request.args.get('value')
    
    if not value or not field_type:
        return jsonify({'exists': False})

    # التأكد من أن الحقل المطلوب فحصه موجود في الموديل
    if hasattr(Supplier, field_type):
        exists = Supplier.query.filter({getattr(Supplier, field_type): value}).first() is not None
        return jsonify({'exists': exists})
    
    return jsonify({'exists': False})
