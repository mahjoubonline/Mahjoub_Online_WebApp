from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from models.supplier_db import db, Supplier

# تعريف الـ Blueprint مع تحديد مجلد القوالب الخاص به
add_supplier_bp = Blueprint(
    'add_supplier', 
    __name__, 
    template_folder='templates'
)

# 1. رابط عرض صفحة إضافة المورد (GET)
@add_supplier_bp.route('/admin/supplier/add', methods=['GET'])
def show_add_page():
    # التحقق من صلاحية المسؤول (اختياري حسب نظامك)
    if not session.get('is_authenticated'):
        return redirect(url_for('auth.login'))

    # حساب المعرف القادم لإظهاره في الواجهة (SUP-MHA_963X)
    last_supplier = Supplier.query.order_by(Supplier.id.desc()).first()
    next_id = (last_supplier.id + 1) if last_supplier else 1
    
    # استدعاء الملف من المسار الذي حددته أنت: admin/dashboard_content.html
    return render_template('admin/dashboard_content.html', next_id=next_id)

# 2. رابط معالجة البيانات وحفظها (POST)
@add_supplier_bp.route('/admin/supplier/save', methods=['POST'])
def save_supplier():
    data = request.get_json()
    
    if not data:
        return jsonify({'status': 'error', 'message': 'بيانات المورد غير مكتملة'}), 400

    try:
        # إنشاء كائن المورد الجديد بناءً على بيانات النموذج
        new_supplier = Supplier(
            username=data.get('username'),
            password=data.get('password'),  # يفضل تشفيرها في المستقبل
            trade_name=data.get('trade_name'),
            owner_name=data.get('owner_name'),
            phone=data.get('phone'),
            activity_type=data.get('activity_type'),
            province=data.get('province'),
            district=data.get('district'),
            address_detail=data.get('address_detail'),
            bank_name=data.get('bank_name'),
            bank_acc=data.get('bank_acc')
        )

        # توليد المعرف السيادي تلقائياً قبل الحفظ
        count = Supplier.query.count() + 1
        new_supplier.sovereign_id = f"SUP-MHA_963{count}"

        db.session.add(new_supplier)
        db.session.commit()

        return jsonify({
            'status': 'success', 
            'message': f'تم تعميد المورد بنجاح بالرقم: {new_supplier.sovereign_id}'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'حدث خطأ في الأرشفة: {str(e)}'}), 500
