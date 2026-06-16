# coding: utf-8
# 📂 apps/add_supplier/routes.py - معالج الأرشفة السيادية

import os
from flask import render_template, request, jsonify, Blueprint
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from apps.models.supplier_db import Supplier
from apps.extensions import db
from apps.config import constants
from datetime import datetime

# تعريف الـ Blueprint
add_supplier_bp = Blueprint('add_supplier_bp', __name__)

# إعداد مسار حفظ الصور
UPLOAD_FOLDER = os.path.join('apps', 'static', 'uploads', 'identities')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@add_supplier_bp.route('/add', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'GET':
        # تمرير next_id كقيمة تجريبية؛ يمكنك جلبها من قاعدة البيانات لاحقاً
        return render_template('admin/add_supplier.html', constants=constants, next_id="963")

    if request.method == 'POST':
        try:
            # 1. استقبال البيانات الأساسية
            username = request.form.get('username')
            password = request.form.get('password')
            
            if not username or not password:
                return jsonify({"status": "error", "message": "بيانات الدخول الأساسية ناقصة"}), 400

            # 2. معالجة صورة الهوية
            identity_image = request.files.get('identity_image')
            image_path = None
            if identity_image:
                filename = secure_filename(f"{username}_{datetime.now().strftime('%Y%m%d')}_{identity_image.filename}")
                save_path = os.path.join(UPLOAD_FOLDER, filename)
                identity_image.save(save_path)
                image_path = filename

            # 3. إنشاء المورد الجديد
            new_supplier = Supplier(
                username=username,
                password_hash=generate_password_hash(password),
                sovereign_id=f"SUP-MHA_963{request.form.get('next_id', '000')}",
                trade_name=request.form.get('trade_name'),
                owner_name=request.form.get('owner_name'),
                id_type=request.form.get('identity_type'),
                supply_category=request.form.get('activity_type'),
                owner_phone=request.form.get('phone'),
                shop_phone=request.form.get('phone'), 
                province=request.form.get('province'),
                district=request.form.get('district'),
                address_detail=request.form.get('address_detail'),
                bank_name=request.form.get('bank_name'),
                bank_acc=request.form.get('bank_acc'),
                # الحقول المضافة للبحث
                search_name=request.form.get('trade_name'),
                search_phone=request.form.get('phone')
            )
            
            # 4. الحفظ في قاعدة البيانات
            db.session.add(new_supplier)
            db.session.commit()
            
            return jsonify({
                "status": "success", 
                "message": "تمت الأرشفة السيادية بنجاح وتشفير كافة البيانات"
            })
            
        except Exception as e:
            db.session.rollback()
            print(f"Error saving supplier: {e}")
            return jsonify({"status": "error", "message": "حدث خطأ أثناء الاتصال بالخزينة المركزية"}), 400
