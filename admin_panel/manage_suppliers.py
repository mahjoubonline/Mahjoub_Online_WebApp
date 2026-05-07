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
<script>
// دالة مراقبة تغيير المحافظة لجلب المديريات من القاعدة
document.getElementById('provinceSelect').addEventListener('change', function() {
    const provinceName = this.value;
    const districtSelect = document.getElementById('districtSelect');
    
    // تفريغ القائمة الحالية
    districtSelect.innerHTML = '<option value="">جاري التحميل...</option>';

    if (!provinceName) {
        districtSelect.innerHTML = '<option value="">اختر المحافظة أولاً</option>';
        return;
    }

    // استدعاء المديريات من السيرفر (القاعدة)
    fetch(`/admin/api/get-districts?province=${provinceName}`)
        .then(res => res.json())
        .then(data => {
            districtSelect.innerHTML = '<option value="">كل المديريات</option>';
            data.districts.forEach(dist => {
                districtSelect.innerHTML += `<option value="${dist}">${dist}</option>`;
            });
        });
});

// دالة فتح لوحة الفحص الجانبية وجلب بيانات المورد التفصيلية
function openSovereignInspector(supplierId) {
    const bsOffcanvas = new bootstrap.Offcanvas(document.getElementById('supplierInspector'));
    bsOffcanvas.show();
    
    fetch(`/admin/api/supplier-details/${supplierId}`)
        .then(res => res.json())
        .then(s => {
            document.getElementById('inspectorContent').innerHTML = `
                <div class="text-center mb-4">
                    <div class="avatar-lrg bg-soft-purple mb-2">
                        <i class="fas fa-store fa-3x text-royal"></i>
                    </div>
                    <h4 class="fw-bold text-royal">${s.trade_name}</h4>
                    <span class="badge bg-gold text-dark">ID: ${s.id}</span>
                </div>
                <ul class="list-group list-group-flush text-end p-0">
                    <li class="list-group-item d-flex justify-content-between small">
                        <span class="fw-bold">${s.phone}</span> :الهاتف
                    </li>
                    <li class="list-group-item d-flex justify-content-between small">
                        <span class="text-primary fw-bold text-ltr">${s.e_wallet || 'لا يوجد'}</span> :المحفظة
                    </li>
                    <li class="list-group-item d-flex justify-content-between small">
                        <span class="text-success fw-bold">${Number(s.balance_yer).toLocaleString()} ر.ي</span> :الرصيد
                    </li>
                </ul>
            `;
            document.getElementById('walletBtn').href = `/admin/wallets/${s.id}`;
        });
}
</script>
