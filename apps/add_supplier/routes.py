# coding: utf-8
# 📂 apps/add_supplier/routes.py

from flask import render_template, request, jsonify
from werkzeug.security import generate_password_hash
from apps.add_supplier import add_supplier_bp
from apps.models.supplier_db import Supplier
from apps.extensions import db
from apps.config import constants

@add_supplier_bp.route('/add', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'GET':
        # تمرير الثوابت للقالب ليتم عرض القوائم المنسدلة (مثل قائمة البنوك والمحافظات)
        return render_template('admin/add_supplier.html', constants=constants, next_id="963")

    if request.method == 'POST':
        data = request.get_json()
        try:
            # التحقق من البيانات الأساسية
            if not data.get('username') or not data.get('password'):
                return jsonify({"status": "error", "message": "بيانات الدخول ناقصة"}), 400

            # إنشاء المورد الجديد
            new_supplier = Supplier(
                username=data['username'],
                password_hash=generate_password_hash(data['password']),
                sovereign_id=f"SUP-MHA_963{data.get('next_id', '000')}",
                trade_name=data.get('trade_name'),
                owner_name=data.get('owner_name'),
                id_type=data.get('identity_type'),
                supply_category=data.get('activity_type'),
                owner_phone=data.get('phone'),
                shop_phone=data.get('phone'), 
                province=data.get('province'),
                district=data.get('district'),
                address_detail=data.get('address_detail'),
                bank_name=data.get('bank_name'),
                bank_acc=data.get('bank_acc')
            )
            
            # الحفظ في قاعدة البيانات
            db.session.add(new_supplier)
            db.session.commit()
            
            return jsonify({
                "status": "success", 
                "message": "تمت الأرشفة السيادية بنجاح وتشفير البيانات"
            })
            
        except Exception as e:
            db.session.rollback()
            # طباعة الخطأ في السجلات لتسهيل التصحيح
            print(f"Error saving supplier: {e}")
            return jsonify({"status": "error", "message": "حدث خطأ أثناء الاتصال بالخزينة المركزية"}), 400
