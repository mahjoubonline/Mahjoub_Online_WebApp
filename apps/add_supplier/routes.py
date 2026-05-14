# coding: utf-8
import os
from flask import render_template, request, jsonify, current_app, Blueprint
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

# استيراد كائن قاعدة البيانات والموديلات
from models.admin_db import db, AdminUser
from models.supplier_db import Supplier

admin_suppliers = Blueprint(
    'admin_suppliers', 
    __name__, 
    template_folder='templates'
)

# إعدادات رفع الملفات لصور الهوية
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin_suppliers.route('/add', methods=['GET', 'POST'])
def add_supplier():
    """
    محرك تعميد الموردين - منظومة محجوب أونلاين السيادية
    استقبال البيانات من واجهة المستخدم ومعالجتها برمجياً
    """
    if request.method == 'POST':
        try:
            # 1. استقبال المعرف السيادي وبيانات الحساب
            unified_id = request.form.get('unified_id')
            username = request.form.get('username')
            password = request.form.get('password')
            
            # 2. بيانات الهوية والنشاط
            id_type = request.form.get('id_type')
            category = request.form.get('category')
            
            # 3. بيانات المالك والاتصال
            owner_name = request.form.get('owner_name')
            trade_name = request.form.get('trade_name')
            owner_phone = request.form.get('owner_phone')
            shop_phone = request.form.get('shop_phone')
            
            # 4. النطاق الجغرافي
            province = request.form.get('province')
            district = request.form.get('district')
            address_detail = request.form.get('address_detail')
            
            # 5. البيانات المالية (معالجة الإدخال اليدوي والقائمة)
            fin_type = request.form.get('fin_type')
            bank_name = request.form.get('bank_name') # سيأتي من الـ select أو الـ input اليدوي برمجياً

            # 6. فحص أمني: هل اسم المستخدم مكرر؟
            existing_user = AdminUser.query.filter_by(username=username).first()
            existing_supp = Supplier.query.filter_by(username=username).first()
            
            if existing_user or existing_supp:
                return jsonify({
                    'status': 'error', 
                    'message': 'اسم المستخدم هذا مسجل مسبقاً في النظام السيادي'
                }), 400

            # 7. معالجة رفع صورة الوثيقة
            identity_image_path = None
            file = request.files.get('identity_image')
            if file and allowed_file(file.filename):
                # تسمية الصورة برقم الهوية السيادي لسهولة الأرشفة
                filename = secure_filename(f"{unified_id}_{file.filename}")
                upload_path = os.path.join(current_app.root_path, 'static/uploads/suppliers/ids')
                
                if not os.path.exists(upload_path):
                    os.makedirs(upload_path)
                
                file.save(os.path.join(upload_path, filename))
                identity_image_path = f"uploads/suppliers/ids/{filename}"

            # 8. إنشاء سجل المورد في قاعدة البيانات (Railway/PostgreSQL)
            new_supplier = Supplier(
                sovereign_id=unified_id,
                username=username,
                password=generate_password_hash(password),
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
                bank_acc=request.form.get('bank_acc'),
                is_active=True
            )

            db.session.add(new_supplier)
            db.session.commit()

            return jsonify({
                'status': 'success', 
                'message': f'تم تعميد المورد "{trade_name}" بنجاح وأرشفة وثائقه'
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'error', 
                'message': f'خطأ في النظام التقني: {str(e)}'
            }), 500

    # طلب العرض (GET): حساب المعرف التسلسلي لعام 2026
    try:
        total_suppliers = Supplier.query.count()
        next_id = total_suppliers + 1
    except:
        next_id = 1
        
    return render_template('admin/add_supplier.html', next_id=next_id)
