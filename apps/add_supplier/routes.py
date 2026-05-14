import os
from flask import render_template, request, jsonify, url_for, current_app, Blueprint
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

# استيراد كائن قاعدة البيانات والموديلات السيادية
from models.admin_db import db, AdminUser
from models.supplier_db import Supplier

# تعريف البلوبرينت
admin_suppliers = Blueprint(
    'admin_suppliers', 
    __name__, 
    template_folder='templates'
)

# إعدادات رفع الملفات (صور الهوية)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin_suppliers.route('/add', methods=['GET', 'POST'])
def add_supplier():
    """
    بوابة إضافة الموردين - منظومة محجوب أونلاين السيادية 2026
    """
    if request.method == 'POST':
        try:
            # 1. استقبال البيانات من النموذج (Frontend)
            unified_id = request.form.get('unified_id')
            username = request.form.get('username')
            password = request.form.get('password')
            id_type = request.form.get('id_type')
            category = request.form.get('category')
            
            owner_name = request.form.get('owner_name')
            trade_name = request.form.get('trade_name')
            owner_phone = request.form.get('owner_phone')
            shop_phone = request.form.get('shop_phone')
            
            province = request.form.get('province')
            district = request.form.get('district')
            address_detail = request.form.get('address_detail')
            
            fin_type = request.form.get('fin_type')
            bank_name = request.form.get('bank_name')
            bank_acc = request.form.get('bank_acc')

            # 2. فحص استباقي لعدم تكرار اليوزر في نظام الإدارة أو الموردين
            user_exists = AdminUser.query.filter_by(username=username).first()
            supp_exists = Supplier.query.filter_by(username=username).first()
            
            if user_exists or supp_exists:
                return jsonify({
                    'status': 'error', 
                    'message': 'عذراً، اسم المستخدم هذا محجوز مسبقاً في النظام السيادي'
                }), 400

            # 3. معالجة رفع صورة الهوية (إن وجدت)
            identity_image_path = None
            file = request.files.get('identity_image')
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{unified_id}_{file.filename}")
                upload_folder = os.path.join(current_app.root_path, 'static/uploads/suppliers/ids')
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                file.save(os.path.join(upload_folder, filename))
                identity_image_path = f"uploads/suppliers/ids/{filename}"

            # 4. أرشفة المورد الجديد في قاعدة البيانات
            new_supplier = Supplier(
                sovereign_id=unified_id,
                username=username,
                password=generate_password_hash(password), # تشفير سيادي للمرور
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
                bank_acc=bank_acc
            )
            
            db.session.add(new_supplier)
            db.session.commit()

            return jsonify({
                'status': 'success', 
                'message': f'تم تعميد المورد "{trade_name}" بنجاح وإصدار الهوية الرقمية له'
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'error', 
                'message': f'فشل في النظام التقني: {str(e)}'
            }), 500

    # معالجة طلب العرض (GET): حساب المعرف القادم
    try:
        # حساب العدد الإجمالي للموردين لإصدار الرقم التسلسلي القادم
        count = Supplier.query.count()
        next_id = count + 1
    except:
        next_id = 1
        
    return render_template('admin/add_supplier.html', next_id=next_id)
