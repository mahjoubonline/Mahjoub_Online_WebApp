from flask import Blueprint, request, jsonify, render_template
from core.extensions import db
from core.models.supplier import Supplier # النموذج الجديد الذي طورناه
from sqlalchemy import or_

# تعريف البلوبرنت
admin_suppliers_bp = Blueprint('admin_suppliers', __name__)

# --- منطق التعميد السيادي (تطوير للكود الخاص بك) ---

def get_all_pending_suppliers():
    """جلب الكيانات التي تنتظر المراجعة والتعميد"""
    # نعتمد هنا على حالة 'audit' أو 'suspended' كحالة انتظار
    return Supplier.query.filter_by(status='audit').all()

@admin_suppliers_bp.route('/admin/api/supplier/approve/<int:sup_id>', methods=['POST'])
def approve_supplier_sovereign(sup_id):
    """بروتوكول التعميد السيادي لتنشيط المورد ومنحه الهوية الرقمية"""
    supplier = Supplier.query.get(sup_id)
    if supplier:
        try:
            supplier.status = 'active'
            # توليد المعرف السيادي WAL_MAH و SUP_MAH تلقائياً عند التعميد
            supplier.mint_sovereign_id() 
            
            db.session.commit()
            return jsonify({"status": "success", "message": f"تم تعميد الكيان {supplier.trade_name} بنجاح"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500
    return jsonify({"status": "error", "message": "المورد غير موجود"}), 404

# --- محرك البحث والجلب (الذي يحتاجه sovereign_engine.js) ---

@admin_suppliers_bp.route('/admin/api/suppliers/search')
def api_search_suppliers():
    query = request.args.get('q', '').strip()
    status = request.args.get('status', '')
    
    search_filter = Supplier.query

    if query:
        search_filter = search_filter.filter(or_(
            Supplier.trade_name.icontains(query),
            Supplier.owner_name.icontains(query),
            Supplier.sovereign_id.icontains(query)
        ))

    if status:
        search_filter = search_filter.filter(Supplier.status == status)

    results = search_filter.order_by(Supplier.id.desc()).all()
    return jsonify([sup.to_dict() for sup in results])

@admin_suppliers_bp.route('/admin/api/supplier/<int:sup_id>')
def api_get_supplier(sup_id):
    """جلب بيانات المورد كاملة للمودال"""
    supplier = Supplier.query.get_or_404(sup_id)
    return jsonify(supplier.to_dict(include_staff=True))

@admin_suppliers_bp.route('/admin/api/supplier/<int:sup_id>/update', methods=['POST'])
def api_update_supplier(sup_id):
    """تحديث البيانات والأرصدة من المودال"""
    supplier = Supplier.query.get_or_404(sup_id)
    data = request.json

    try:
        supplier.owner_name = data.get('owner_name')
        supplier.trade_name = data.get('trade_name')
        supplier.balance_yer = data.get('balance_yer', 0)
        supplier.balance_sar = data.get('balance_sar', 0)
        supplier.balance_usd = data.get('balance_usd', 0)
        supplier.status = data.get('status')
        supplier.tier = data.get('tier')

        if data.get('new_password'):
            supplier.set_password(data.get('new_password'))

        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
