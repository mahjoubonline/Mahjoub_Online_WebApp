# coding: utf-8
# 🔑 الجزء المطور لمعالجة رفع الملفات والنصوص معاً في محرك الموردين

import os
from werkzeug.utils import secure_filename
from flask import current_app, jsonify, request, render_template
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from apps import db
from apps.models import Supplier
from textwrap import dedent

# امتدادات الصور المسموح بها حوكمياً
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin_suppliers.route('/add', methods=['GET', 'POST'], endpoint='add_supplier_page')
@admin_suppliers.route('/add_legacy', methods=['GET', 'POST'], endpoint='add_supplier')
@login_required
def add_supplier_page():
    if request.method == 'POST':
        try:
            # 1. استقبال الحقول النصية السبعة المطهّرة
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            identity_type = request.form.get('identity_type', '').strip()
            identity_number = request.form.get('identity_number', '').strip()
            owner_name = request.form.get('owner_name', '').strip()
            trade_name = request.form.get('trade_name', '').strip()
            owner_phone = request.form.get('owner_phone', '').strip()
            shop_phone = request.form.get('shop_phone', '').strip()
            province = request.form.get('province', '').strip()
            district = request.form.get('district', '').strip()
            address_detail = request.form.get('address_detail', '').strip()
            fin_type = request.form.get('fin_type', '').strip()
            bank_name = request.form.get('bank_name', '').strip()
            bank_acc = request.form.get('bank_acc', '').strip()
            activity_type = request.form.get('activity_type', '').strip()
            user_rank = request.form.get('user_rank', 'ريادي').strip()

            # التحقق الفوري الحوكمي من عدم إرسال حقول أساسية فارغة
            required_post_fields = {
                "username": username, "identity_number": identity_number, 
                "owner_name": owner_name, "trade_name": trade_name, 
                "owner_phone": owner_phone, "shop_phone": shop_phone, "bank_acc": bank_acc
            }
            for f_key, f_val in required_post_fields.items():
                if not f_val:
                    return jsonify({"status": "error", "message": f"تنبيه سيادي: الحقل الأساسي ({f_key}) فارغ."}), 400

            # 2. فحص الحقول السبعة في الخلفية لمنع التكرار
            check_fields = {
                "username": (db.session.query(Supplier.id).filter_by(username=username).first(), "اسم المستخدم (Login)"),
                "identity_number": (db.session.query(Supplier.id).filter_by(identity_number=identity_number).first(), "رقم الوثيقة / الهوية"),
                "owner_name": (db.session.query(Supplier.id).filter_by(owner_name=owner_name).first(), "اسم المالك الكامل"),
                "trade_name": (db.session.query(Supplier.id).filter_by(trade_name=trade_name).first(), "الاسم التجاري للمنشأة"),
                "owner_phone": (db.session.query(Supplier.id).filter_by(owner_phone=owner_phone).first(), "رقم هاتف المالك"),
                "shop_phone": (db.session.query(Supplier.id).filter_by(shop_phone=shop_phone).first(), "هاتف المنشأة (محل)"),
                "bank_acc": (db.session.query(Supplier.id).filter_by(bank_acc=bank_acc).first(), "رقم الحساب")
            }
            for key, (exists, field_title) in check_fields.items():
                if exists:
                    return jsonify({"status": "error", "message": f"تنبيه حوكمي: حقل ({field_title}) مسجل مسبقاً."}), 400

            # 3. معالجة رفع وثيقة الهوية بأمان (اختياري)
            identity_card_img = None
            if 'identity_card_img' in request.files:
                file = request.files['identity_card_img']
                if file and file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    # توليد اسم فريد يمنع التداخل بربطه باسم المستخدم
                    unique_filename = f"{username}_{filename}"
                    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'identity_docs')
                    
                    # إنشاء المجلد إن لم يكن موجوداً على السيرفر
                    os.makedirs(upload_folder, exist_ok=True)
                    
                    file.save(os.path.join(upload_folder, unique_filename))
                    identity_card_img = f"uploads/identity_docs/{unique_filename}"

            # 4. بناء كائن المورد وتشفير كلمة المرور
            hashed_password = generate_password_hash(password)
            new_supplier = Supplier(
                username=username,
                password_hash=hashed_password,
                identity_type=identity_type,
                identity_number=identity_number,
                owner_name=owner_name,
                trade_name=trade_name,
                owner_phone=owner_phone,
                shop_phone=shop_phone,
                province=province,
                district=district,
                address_detail=address_detail,
                fin_type=fin_type,
                bank_name=bank_name,
                bank_acc=bank_acc,
                activity_type=activity_type,
                identity_card_img=identity_card_img, # حفظ مسار الصورة بالسيرفر
                registration_source='لوحة التحكم',
                rank_grade=user_rank,         
                status='active',         
                created_by_id=current_user.id if hasattr(current_user, 'id') else None
            )

            db.session.add(new_supplier)
            db.session.flush()  

            # 5. 💳 توليد المحفظة المالية النظيفة بالاعتماد الكامل على القيم الافتراضية لقاعدة البيانات
            insert_query = db.text(dedent("""
                INSERT INTO supplier_wallets (supplier_id) 
                VALUES (:supplier_id)
            """))
            db.session.execute(insert_query, {"supplier_id": new_supplier.id})
            
            db.session.commit()
            return jsonify({"status": "success", "message": "تم تعميد المورد بنجاح وتنشيط محفظته المالية الحوكمية."}), 200

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"❌ خطأ بنيوي أثناء حفظ المورد: {str(e)}")
            return jsonify({"status": "error", "message": f"حدث خطأ غير متوقع: {str(e)}"}), 500

    # مرحلة الـ GET لعرض الواجهة
    sovereign_id = get_expected_sovereign_id()
    return render_template('admin/add_supplier.html', sovereign_id=sovereign_id, owner=current_user)
