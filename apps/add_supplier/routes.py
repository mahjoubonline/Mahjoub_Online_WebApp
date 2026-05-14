# coding: utf-8
import os
from flask import render_template, request, jsonify, current_app, Blueprint
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

# استيراد كائن قاعدة البيانات والموديلات لضمان وحدة البيانات السيادية
from models.admin_db import db, AdminUser
from models.supplier_db import Supplier

# تعريف الـ Blueprint الخاص بإدارة الموردين
admin_suppliers = Blueprint(
    'admin_suppliers', 
    __name__, 
    template_folder='templates'
)

# إعدادات أمان رفع الملفات لصور الهوية والوثائق
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    """التحقق من امتداد الملف لضمان أمن النظام"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin_suppliers.route('/add', methods=['GET', 'POST'])
def add_supplier():
    """
    محرك تعميد الموردين - منظومة محجوب أونلاين السيادية
    معالجة البيانات ومنع التكرار (الهاتف، الاسم التجاري، الحساب) لضمان سلامة الأرشفة
    """
    if request.method == 'POST':
        try:
            # 1. استقبال المعرف السيادي وبيانات الوصول
            unified_id = request.form.get('unified_id')
            username = request.form.get('username')
            password = request.form.get('password') # نحفظ الأصل مؤقتاً لإرساله في الرد قبل التشفير
            
            # 2. بيانات الهوية والنشاط التجاري
            id_type = request.form.get('id_type')
            category = request.form.get('category')
            
            # 3. بيانات المالك والاتصال الرسمية
            owner_name = request.form.get('owner_name')
            trade_name = request.form.get('trade_name')
            owner_phone = request.form.get('owner_phone')
            shop_phone = request.form.get('shop_phone')
            
            # 4. التوزيع الجغرافي (النطاق السيادي)
            province = request.form.get('province')
            district = request.form.get('district')
            address_detail = request.form.get('address_detail')
            
            # 5. البيانات المالية (الربط البنكي)
            fin_type = request.form.get('fin_type')
            bank_name = request.form.get('bank_name')
            bank_acc = request.form.get('bank_acc')

            # --- 6. الفحص الأمني المكثف: منع تكرار البيانات الحساسة ---
            
            # أ. فحص اسم المستخدم (في جداول الإدمن والموردين)
            if AdminUser.query.filter_by(username=username).first() or \
               Supplier.query.filter_by(username=username).first():
                return jsonify({'status': 'error', 'message': f'اسم المستخدم ({username}) مسجل مسبقاً. يرجى اختيار اسم آخر.'}), 400
            
            # ب. فحص رقم الهاتف (لمنع تكرار تسجيل المالك)
            if Supplier.query.filter_by(owner_phone=owner_phone).first():
                return jsonify({'status': 'error', 'message': f'رقم الهاتف ({owner_phone}) مرتبط بمورد آخر بالفعل.'}), 400
            
            # ج. فحص الاسم التجاري للمنشأة
            if Supplier.query.filter_by(trade_name=trade_name).first():
                return jsonify({'status': 'error', 'message': f'الاسم التجاري ({trade_name}) معمد مسبقاً في النظام.'}), 400

            # --- 7. معالجة وأرشفة صور الوثائق الرسمية ---
            identity_image_path = None
            file = request.files.get('identity_image')
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{unified_id}_{file.filename}")
                upload_path = os.path.join(current_app.root_path, 'static/uploads/suppliers/ids')
                
                if not os.path.exists(upload_path):
                    os.makedirs(upload_path)
                
                file.save(os.path.join(upload_path, filename))
                identity_image_path = f"uploads/suppliers/ids/{filename}"

            # --- 8. حفظ السجل الجديد في قاعدة البيانات السيادية ---
            new_supplier = Supplier(
                sovereign_id=unified_id,
                username=username,
                password=generate_password_hash(password), # التشفير قبل الحفظ
                identity_type=id_type,
                activity_type=category,
                identity_image=identity_image_path,
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
                is_active=True
            )

            db.session.add(new_supplier)
            db.session.commit()

            # --- 9. رد النجاح مع بيانات النسخ للموظف ---
            return jsonify({
                'status': 'success', 
                'message': 'تم الاعتماد بنجاح',
                'data': {
                    'username': username,
                    'password': password, # إرجاع الكلمة الأصلية للنسخ فقط في هذه اللحظة
                    'trade_name': trade_name,
                    'unified_id': unified_id
                }
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'error', 
                'message': f'فشل في معالجة البيانات: {str(e)}'
            }), 500

    # طلب العرض (GET): حساب الرقم التسلسلي التالي
    try:
        total_suppliers = Supplier.query.count()
        next_id = total_suppliers + 1
    except Exception:
        next_id = 1
        
    return render_template('admin/add_supplier.html', next_id=next_id)
