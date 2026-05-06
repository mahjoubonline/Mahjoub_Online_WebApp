# admin_panel/manage_suppliers.py
from flask import request, jsonify
from flask_login import login_required, current_user
from core.extensions import db
from core.models.supplier import Supplier
from . import admin_bp

# --- بروتوكول التحقق السيادي ---
def is_admin_sovereign():
    """ يضمن أن علي محجوب فقط هو من يدير الترددات الميدانية. """
    return current_user.is_authenticated and getattr(current_user, 'role', '').lower() == 'admin'

# --- 1. بروتوكول السحب الذكي (من جدول Supplier الأساسي) ---
@admin_bp.route('/api/supplier/fetch', methods=['POST'])
@login_required
def fetch_supplier_data():
    if not is_admin_sovereign():
        return jsonify({'status': 'error', 'message': 'صلاحية مرفوضة'}), 403
    
    data = request.json
    search_query = data.get('query', '')

    # البحث باستخدام المعرف أو رقم الهاتف (بروتوكول 963)
    # نسحب هنا من جدول "Supplier" الأصلي مباشرة دون إنشاء جدول جديد
    supplier = Supplier.query.filter(
        (Supplier.id == search_query.replace('963', '')) | 
        (Supplier.phone == search_query)
    ).first()

    if not supplier:
        return jsonify({'status': 'error', 'message': 'المورد غير مسجل في القاعدة'}), 404

    # إرسال البيانات لتعبئة التصميم الأفقي
    return jsonify({
        'status': 'success',
        'data': {
            'id': supplier.id,
            'phone': supplier.phone,
            'activity': supplier.activity_type,
            'province': supplier.province,
            'tier': supplier.tier,  # يسحب الرتبة التي أضفناها للنواة
            'status': supplier.status
        }
    })

# --- 2. بروتوكول تحديث البيانات (دون تكرار) ---
@admin_bp.route('/api/supplier/update_field', methods=['POST'])
@login_required
def update_supplier_field():
    if not is_admin_sovereign():
        return jsonify({'status': 'error', 'message': 'غير مصرح بالتعديل'}), 403
    
    data = request.json
    supplier = Supplier.query.get(data.get('id'))

    if not supplier:
        return jsonify({'status': 'error', 'message': 'فشل العثور على المورد'}), 404

    try:
        # تحديث الحقول في الجدول الأساسي مباشرة
        supplier.phone = data.get('phone')
        supplier.activity_type = data.get('activity')
        supplier.province = data.get('province')
        supplier.tier = data.get('tier')
        supplier.status = data.get('status')

        db.session.commit() # تعميد التغييرات في القاعدة الأصلية
        return jsonify({'status': 'success', 'message': 'تم تحديث التردد بنجاح ✅'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'خطأ: {str(e)}'}), 400
