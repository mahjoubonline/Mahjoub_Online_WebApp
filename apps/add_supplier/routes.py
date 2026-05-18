import os
import secrets
from flask import Blueprint, render_template, request, jsonify, current_app, url_for
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

# استيراد كائن قاعدة البيانات المركزي والنماذج
from apps import db
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import Wallet

# 🛡️ تعريف الـ Blueprint الخاص بإضافة وتعميد الموردين
admin_suppliers_bp = Blueprint(
    'admin_suppliers', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ─── المسارات (Routes) ───

@admin_suppliers_bp.route('/admin/suppliers/add', methods=['GET', 'POST'])
def add_supplier_page():
    """
    عرض صفحة تعميد المورد المعالجة السحابية الفعالة للحفظ والربط الحصين.
    """
    # 🚀 هندسة الإصلاح الذاتي لضمان وجود حقل wallet_code في قاعدة البيانات
    try:
        db.session.execute(db.text("ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS wallet_code VARCHAR(50) UNIQUE;"))
        db.session.commit()
    except Exception:
        db.session.rollback()

    if request.method == 'POST':
        try:
            # 1. استقبال البيانات الأساسية من النموذج وتنظيفها
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

            # 2. التحقق الخلفي الصارم من الحقول الإلزامية
            if not all([username, password, identity_type, identity_number, owner_name, trade_name, owner_phone, province, district, address_detail, bank_name, bank_acc]):
                return jsonify({
                    "status": "error",
                    "message": "⚠️ جميع الحقول الإلزامية يجب أن تكون مكتملة وصحيحة هندسيًا."
                }), 400

            # 3. التحقق من عدم التكرار
            if Supplier.query.filter_by(username=username).first():
                return jsonify({"status": "error", "message": "اسم المستخدم هذا محجوز مسبقاً بالتشفير السيادي."}), 400
            
            if Supplier.query.filter_by(identity_number=identity_number).first():
                return jsonify({"status": "error", "message": "رقم الوثيقة / الهوية مسجل مسبقاً في النظام."}), 400

            # 4. معالجة رفع صورة الوثيقة
            identity_image_db_path = None
            if 'identity_image' in request.files:
                file = request.files['identity_image']
                if file and file.filename != '':
                    if allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        unique_filename = f"doc_{secrets.token_hex(8)}_{filename}"
                        base_upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'identities')
                        os.makedirs(base_upload_folder, exist_ok=True)
                        file.save(os.path.join(base_upload_folder, unique_filename))
                        identity_image_db_path = f"uploads/identities/{unique_filename}"

            # 5. توليد المعرف الديناميكي الموحد للمورد واستبداله للمحفظة
            generated_sovereign_id = Supplier.generate_next_sovereign_id()
            
            # 🔄 تبديل البادئة تلقائياً من SUP إلى WEL للمحفظة نفس رقم الأيدي تماماً
            if generated_sovereign_id.startswith("SUP-"):
                generated_wallet_code = generated_sovereign_id.replace("SUP-", "WEL-", 1)
            else:
                generated_wallet_code = f"WEL-{generated_sovereign_id}"

            # 6. تشفير كلمة المرور لحماية الهوية الرقمية للمورد
            hashed_password = generate_password_hash(password)

            # 7. إنشاء المورد وإضافته للمرحلة الأولى
            new_supplier = Supplier(
                username=username,
                password_hash=hashed_password,  
                sovereign_id=generated_sovereign_id,
                wallet_code=generated_wallet_code,
                identity_type=identity_type,
                identity_number=identity_number,
                identity_image=identity_image_db_path,
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
                status="نشط"
            )
            db.session.add(new_supplier)
            
            # ⚡ خطوة ذهبية: حجز معرف المورد داخل الجلسة فوراً (Flush) لمنع قيد القيد الأجنبي الخارجي f405
            db.session.flush()

            # 8. بناء المحفظة المالية المتكاملة وتمرير الحقول الأساسية النظيفة فقط
            wallet_args = {
                "wallet_code": generated_wallet_code,
                "supplier_id": generated_sovereign_id  # تم الفتح والحجز بنجاح الآن
            }

            # تصفير الأرصدة الإجمالية الحقيقية للعملات الثلاث بشكل صريح وآمن
            for raw_field in ['yer_total', 'sar_total', 'usd_total']:
                if hasattr(Wallet, raw_field) and not isinstance(getattr(Wallet, raw_field), property):
                    wallet_args[raw_field] = 0.0

            # وضع الحالة الافتراضية
            if hasattr(Wallet, 'status') and not isinstance(getattr(Wallet, 'status'), property):
                wallet_args['status'] = "نشطة"

            new_wallet = Wallet(**wallet_args)
            db.session.add(new_wallet)

            # 9. تنفيذ الحفظ الموحد النهائي (Atomic Commit) لتعميد المورد ومحفظته معاً
            db.session.commit()

            return jsonify({
                "status": "success",
                "message": "تم الحفظ الفعلي وتعميد المحفظة التلقائية بنجاح مطلق.",
                "data": {
                    "sovereign_id": generated_sovereign_id,
                    "wallet_code": generated_wallet_code
                }
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({
                "status": "error",
                "message": f"فشل داخلي في السيرفر السحابي (500): {str(e)}"
            }), 500

    # في حالة طلب الصفحة عبر (GET)
    endpoints_config = {
        "add_supplier": url_for('admin_suppliers.add_supplier_page'),
        "check_duplicate": url_for('admin_suppliers.check_duplicate')
    }
    return render_template('admin/add_supplier.html', endpoints=endpoints_config)


@admin_suppliers_bp.route('/admin/suppliers/check-duplicate', methods=['GET'])
def check_duplicate():
    check_type = request.args.get('type', '')
    value = request.args.get('value', '').strip()

    if not check_type or not value or check_type not in ['username', 'identity_number', 'owner_phone', 'trade_name', 'bank_acc']:
        return jsonify({"exists": False, "error": "المعاملات البرمجية غير مدعومة"}), 400

    try:
        exists = db.session.query(Supplier).filter(getattr(Supplier, check_type) == value).first() is not None
        return jsonify({"exists": bool(exists)})
    except Exception:
        return jsonify({"exists": False, "error": "فشل فحص قاعدة البيانات"})
