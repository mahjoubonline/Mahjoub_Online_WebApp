import os
from flask import render_template, request, jsonify, url_for, current_app, Blueprint
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

# استيراد كائن قاعدة البيانات والموديلات السيادية من الجذر
from models.admin_db import db, AdminUser
from models.supplier_db import Supplier

# إصلاح الاستيراد الدائري: تعريف البلوبرينت هنا مباشرة بدلاً من __init__.py
admin_suppliers = Blueprint(
    'admin_suppliers', 
    __name__, 
    template_folder='templates'
)

@admin_suppliers.route('/add', methods=['GET', 'POST'])
def add_supplier():
    """
    بوابة إضافة الموردين - منظومة محجوب أونلاين السيادية
    """
    if request.method == 'POST':
        try:
            # 1. استقبال البيانات من النموذج الرقمي
            username = request.form.get('username')
            password = request.form.get('password')
            trade_name = request.form.get('trade_name')
            owner_name = request.form.get('owner_name')
            phone = request.form.get('phone')
            province = request.form.get('province')
            bank_acc = request.form.get('bank_acc')

            # 2. فحص استباقي لعدم تكرار الهوية الرقمية في جدول المسؤولين
            exists = AdminUser.query.filter_by(username=username).first()
            if exists:
                return jsonify({
                    'status': 'error', 
                    'message': 'عذراً، اسم المستخدم هذا محجوز مسبقاً في النظام السيادي'
                }), 400

            # 3. أرشفة المورد الجديد في قاعدة البيانات (PostgreSQL/Railway)
            new_supplier = Supplier(
                username=username,
                password=generate_password_hash(password),
                trade_name=trade_name,
                owner_name=owner_name,
                phone=phone,
                province=province,
                bank_acc=bank_acc
            )
            
            db.session.add(new_supplier)
            db.session.commit()

            return jsonify({
                'status': 'success', 
                'message': f'تم تعميد المورد "{trade_name}" بنجاح وأرشفة بياناته'
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'error', 
                'message': f'فشل في النظام التقني: {str(e)}'
            }), 500

    # 4. معالجة طلب العرض (GET): حساب المعرف القادم لإظهاره في الواجهة
    try:
        next_id = Supplier.query.count() + 1
    except:
        next_id = 1
        
    return render_template('admin/add_supplier.html', next_id=next_id)
