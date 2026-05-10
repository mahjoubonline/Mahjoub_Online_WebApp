# admin_panel/add_supplier_routes.py
from flask import render_template, request, jsonify
from flask_login import login_required
from . import admin_bp
from .engines.supplier_engine import create_new_supplier  # استدعاء المحرك السيادي

@admin_bp.route('/suppliers/add', methods=['GET', 'POST'])
@login_required
def add_supplier():
    """مسار التعميد السيادي للموردين"""
    if request.method == 'POST':
        # نرسل البيانات للمحرك وننتظر النتيجة
        success, result = create_new_supplier(request.form)
        
        if success:
            return jsonify({
                "status": "success", 
                "message": f"تم التعميد بنجاح! المعرف السيادي: {result}"
            })
        else:
            return jsonify({
                "status": "error", 
                "message": f"فشل التعميد: {result}"
            }), 500

    # في حالة GET: عرض صفحة الإضافة
    from core.models.supplier import Supplier
    last_s = Supplier.query.order_by(Supplier.id.desc()).first()
    next_id = (last_s.id + 1) if last_s else 1
    return render_template('admin/add_supplier.html', next_id=next_id)
