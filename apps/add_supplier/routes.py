from flask import render_template, request, jsonify
from werkzeug.security import generate_password_hash
from apps.add_supplier import add_supplier_bp
from apps.models.supplier_db import Supplier
from apps.extensions import db
from apps.config import constants

@add_supplier_bp.route('/add', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'GET':
        return render_template('admin/add_supplier.html', constants=constants, next_id="963")

    if request.method == 'POST':
        data = request.get_json()
        try:
            # 1. إنشاء المورد الجديد
            new_supplier = Supplier(
                username=data['username'],
                password_hash=generate_password_hash(data['password']),
                # تعيين القيم سيقوم تلقائياً بتشغيل الـ setter المشفر في الموديل
                sovereign_id=f"SUP-MHA_963{data.get('next_id', '000')}",
                trade_name=data['trade_name'],
                owner_name=data['owner_name'],
                id_type=data['identity_type'],
                supply_category=data['activity_type'],
                owner_phone=data['phone'],
                shop_phone=data['phone'], # إذا كان هناك حقلين للهاتف
                province=data['province'],
                district=data['district'],
                address_detail=data['address_detail'],
                bank_name=data['bank_name'],
                bank_acc=data['bank_acc']
            )
            
            # 2. الحفظ في قاعدة البيانات
            db.session.add(new_supplier)
            db.session.commit()
            
            return jsonify({"status": "success", "message": "تمت الأرشفة السيادية بنجاح وتشفير البيانات"})
            
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 400
