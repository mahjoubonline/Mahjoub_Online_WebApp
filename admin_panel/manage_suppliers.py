from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from core.extensions import db
from core.models.supplier import Supplier
from . import admin_bp

# --- بروتوكول التحقق السيادي ---
def is_admin_sovereign():
    """ يضمن أن المؤسس علي محجوب فقط هو من يدير الترددات الميدانية. """
    return current_user.is_authenticated and getattr(current_user, 'role', '').lower() == 'admin'

# --- 1. عرض النافذة (The View) ---
@admin_bp.route('/manage-suppliers')
@login_required
def manage_suppliers_view():
    if not is_admin_sovereign():
        return redirect(url_for('admin.login'))
    return render_template('manage_suppliers.html')

# --- 2. بروتوكول السحب الميداني (Fetch from COR) ---
@admin_bp.route('/api/supplier/fetch', methods=['POST'])
@login_required
def fetch_supplier_data():
    if not is_admin_sovereign():
        return jsonify({'status': 'error', 'message': 'صلاحية مرفوضة'}), 403
    
    data = request.json
    search_query = data.get('query', '')

    # تنظيف المدخلات للبحث بالترقيم السيادي 963
    clean_id = search_query.replace('963', '')

    # البحث في القاعدة (سحب البيانات الحيوية)
    supplier = Supplier.query.filter(
        (Supplier.id == clean_id) | 
        (Supplier.phone == search_query) |
        (Supplier.trade_name.like(f"%{search_query}%"))
    ).first()

    if not supplier:
        return jsonify({'status': 'error', 'message': 'الكيان غير موجود في القاعدة'}), 404

    # إرسال البيانات لتعبئة الخانات في الصورة image_86bfc7.png
    return jsonify({
        'status': 'success',
        'data': {
            'id': supplier.id,
            'full_id': f"SUP-MAH-963{supplier.id}",
            'phone': supplier.phone,
            'activity': supplier.activity_type,
            'province': supplier.province,
            'tier': getattr(supplier, 'tier', 'مبتدئ'), # سحب الرتبة
            'status': getattr(supplier, 'status', 'active'), # سحب الحالة الإدارية
            'trade_name': supplier.trade_name
        }
    })

# --- 3. بروتوكول التحديث والمزامنة (Sync to COR) ---
@admin_bp.route('/api/supplier/update_field', methods=['POST'])
@login_required
def update_supplier_field():
    if not is_admin_sovereign():
        return jsonify({'status': 'error', 'message': 'غير مصرح لك بالتعديل'}), 403
    
    data = request.json
    supplier = Supplier.query.get(data.get('id'))

    if not supplier:
        return jsonify({'status': 'error', 'message': 'فشل العثور على الكيان'}), 404

    try:
        # تحديث الحقول الظاهرة في نافذة التردد الميداني
        supplier.phone = data.get('phone')
        supplier.activity_type = data.get('activity')
        supplier.province = data.get('province')
        
        # تحديث الرتبة والحالة (إذا كانت مدعومة في COR)
        if hasattr(supplier, 'tier'): supplier.tier = data.get('tier')
        if hasattr(supplier, 'status'): supplier.status = data.get('status')

        db.session.commit()
        return jsonify({'status': 'success', 'message': f'تم تحديث بيانات "{supplier.trade_name}" بنجاح ✅'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'خطأ في المزامنة: {str(e)}'}), 400
