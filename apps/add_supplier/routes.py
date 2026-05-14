import os
from flask import Blueprint, render_template, request, jsonify, current_app
from datetime import datetime
from werkzeug.utils import secure_filename

# استيراد قاعدة البيانات والموديل من المسار الذي حددته
from models.supplier_db import db, Supplier 

# تعريف الـ Blueprint مع تحديد مسار المجلدات إذا كان الهيكل مخصصاً
admin_suppliers = Blueprint(
    'admin_suppliers', 
    __name__,
    template_folder='../../templates' # تأكد أن هذا يشير لمجلد القوالب الرئيسي
)

@admin_suppliers.route('/admin/suppliers/add', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        try:
            # 1. استلام البيانات من النموذج
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
            address_detail = request.form.get('address_detail')

            fin_type = request.form.get('fin_type')
            bank_name = request.form.get('bank_name')
            bank_acc = request.form.get('bank_acc')

            # 2. إنشاء السجل وحفظه
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
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'message': f'خطأ في النظام: {str(e)}'
            }), 400

    # في حالة GET: معالجة المعرف التسلسلي
    try:
        last_supplier = Supplier.query.order_by(Supplier.id.desc()).first()
        next_id_num = (last_supplier.id + 1) if last_supplier else 1
    except:
        next_id_num = 1
        
    # ملاحظة: تأكد أن الملف موجود في templates/admin/add_supplier.html
    return render_template('admin/add_supplier.html', next_id=next_id_num)
