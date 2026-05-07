from flask import render_template, request, jsonify
from sqlalchemy import or_, cast, String
from core.models.supplier import Supplier
from core.extensions import db
from . import admin_bp
from flask_login import login_required, current_user
from functools import wraps

# --- 1. بروتوكول الحماية السيادي ---
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # التأكد أن المستخدم هو "علي محجوب" أو يحمل رتبة admin
        if not current_user.is_authenticated or getattr(current_user, 'role', '').lower() != 'admin':
            return jsonify({"status": "error", "message": "غير مسموح بالوصول لهذا المستوى"}), 403
        return f(*args, **kwargs)
    return decorated_function

# قائمة الجغرافيا المركزية لليمن (Sovereign Geography Registry)
YEMEN_GEOGRAPHY = {
    "الحديدة": ["الخوخة", "حيس", "الحوك", "الميناء", "زبيد", "بيت الفقيه"],
    "أمانة العاصمة": ["السبعين", "التحرير", "الثورة", "صنعاء القديمة"],
    "عدن": ["المنصورة", "كريتر", "الشيخ عثمان", "البريقة"],
    "تعز": ["المخاء", "القاهرة", "المظفر"]
}

# --- 2. عرض الواجهة الرئيسية للإدارة ---
@admin_bp.route('/manage-suppliers')
@login_required
def manage_suppliers():
    """عرض صفحة الترسانة مع تحميل أولي للموردين"""
    # جلب آخر 20 مورد لضمان سرعة الاستجابة عند الفتح
    initial_suppliers = Supplier.query.order_by(Supplier.id.desc()).limit(20).all()
    
    return render_template(
        'manage_suppliers.html', 
        suppliers=initial_suppliers,
        provinces_list=YEMEN_GEOGRAPHY.keys()
    )

# --- 3. محرك البحث الذكي (The Sovereign Search Engine) ---
@admin_bp.route('/api/search-suppliers')
@login_required
def api_search_suppliers():
    """منطق البحث المتقدم بالفلاتر (AJAX) لربط القالب بالقاعدة"""
    q = request.args.get('q', '').strip()
    province = request.args.get('province', '').strip()
    district = request.args.get('district', '').strip()

    query_obj = Supplier.query

    # البحث النصي الشامل (اسم المتجر، اسم المالك، الهاتف، المعرف السيادي)
    if q:
        clean_q = q.replace('SUP-MAH-', '').replace('WAL-MAH-', '')
        query_obj = query_obj.filter(
            or_(
                Supplier.trade_name.ilike(f"%{q}%"),
                Supplier.owner_name.ilike(f"%{q}%"),
                Supplier.phone.ilike(f"%{q}%"),
                Supplier.e_wallet.ilike(f"%{q}%"),
                cast(Supplier.id, String).ilike(f"%{clean_q}%")
            )
        )

    # فلاتر الموقع الجغرافي
    if province:
        query_obj = query_obj.filter_by(province=province)
    if district:
        query_obj = query_obj.filter_by(district=district)

    suppliers = query_obj.order_by(Supplier.id.desc()).all()
    
    return jsonify({
        "status": "success",
        "count": len(suppliers),
        "suppliers": [s.to_dict() for s in suppliers]
    })

# --- 4. جلب بيانات المورد التفصيلية (للمودال) ---
@admin_bp.route('/api/supplier-details/<int:s_id>')
@login_required
@admin_required
def get_supplier_details(s_id):
    """سحب بيانات مورد واحد لملء قالب الإحصائيات"""
    supplier = Supplier.query.get_or_404(s_id)
    return jsonify({
        "id": supplier.id,
        "trade_name": supplier.trade_name,
        "owner_name": supplier.owner_name,
        "phone": supplier.phone,
        "e_wallet": supplier.e_wallet or f"WAL-MAH-{supplier.id}",
        "balance_yer": float(supplier.balance_yer or 0),
        "status": supplier.status,
        "province": supplier.province,
        "district": supplier.district
    })

# --- 5. تحديث البيانات السيادية (إدارة المالك، الهاتف، وكلمة المرور) ---
@admin_bp.route('/api/update-supplier-info/<int:s_id>', methods=['POST'])
@login_required
@admin_required
def update_supplier_info(s_id):
    """تعديل بيانات المورد من داخل القالب مباشرة"""
    supplier = Supplier.query.get_or_404(s_id)
    data = request.get_json()

    # تحديث الحقول الأساسية
    if 'owner_name' in data: supplier.owner_name = data['owner_name']
    if 'phone' in data: supplier.phone = data['phone']
    
    # إعادة تعيين كلمة المرور في حال تم إدخال قيمة جديدة
    password = data.get('password')
    if password and len(password) >= 6:
        supplier.set_password(password) # استخدام التشفير المعتمد في الموديل

    try:
        db.session.commit()
        return jsonify({"status": "success", "message": "تم تعميد البيانات الجديدة في الترسانة"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

# --- 6. بوابة التحكم في الحالة (تفعيل/تعليق) ---
@admin_bp.route('/api/toggle-supplier-status/<int:s_id>', methods=['POST'])
@login_required
@admin_required
def toggle_status(s_id):
    """تغيير حالة المورد بين نشط ومعلق"""
    supplier = Supplier.query.get_or_404(s_id)
    data = request.get_json()
    new_status = data.get('status')

    if new_status in ['active', 'suspended']:
        supplier.status = new_status
        db.session.commit()
        return jsonify({"status": "success", "message": f"تم تحديث حالة {supplier.trade_name}"})
    
    return jsonify({"status": "error", "message": "حالة غير صالحة"}), 400

# --- 7. بروتوكول الشطب (حذف المورد) ---
@admin_bp.route('/api/delete-supplier/<int:s_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_supplier(s_id):
    """حذف المورد نهائياً من قاعدة البيانات"""
    supplier = Supplier.query.get_or_404(s_id)
    
    # إجراء وقائي: منع حذف المورد إذا كان لديه رصيد مالي
    if (supplier.balance_yer or 0) > 0:
        return jsonify({"status": "error", "message": "لا يمكن شطب كيان لديه رصيد مالي نشط"}), 400

    try:
        db.session.delete(supplier)
        db.session.commit()
        return jsonify({"status": "success", "message": "تم شطب الكيان بنجاح"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": "خطأ في عملية الحذف"}), 500

# --- 8. جلب المديريات ديناميكياً ---
@admin_bp.route('/api/get-districts')
def get_districts():
    province = request.args.get('province')
    districts = YEMEN_GEOGRAPHY.get(province, [])
    return jsonify(districts)
