# admin_panel/add_supplier_routes.py
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from admin_panel.suppliers_logic import SupplierLogic
from admin_panel import admin_bp

# ==========================================
# 1. نافذة تعميد مورد جديد (Add Supplier)
# ==========================================
@admin_bp.route('/suppliers/add', methods=['GET', 'POST'])
@login_required
def add_supplier():
    if request.method == 'POST':
        # إرسال البيانات للمحرك الذكي
        success, message = SupplierLogic.register_supplier(request.form)
        
        # إذا كان الطلب قادماً من JavaScript (AJAX)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': success, 'message': message})
        
        # إذا كان طلباً عادياً
        flash(message, 'success' if success else 'danger')
        if success:
            return redirect(url_for('admin.manage_suppliers'))
            
    # جلب المعرف القادم SUP_# لعرضه في الواجهة
    next_id = SupplierLogic.get_next_id()
    return render_template('admin/add_supplier.html', next_id=next_id)

# ==========================================
# 2. رادار إدارة الموردين (Manage Suppliers)
# ==========================================
@admin_bp.route('/suppliers/manage')
@login_required
def manage_suppliers():
    # محرك البحث والفرز
    search_query = request.args.get('search')
    status_filter = request.args.get('status')
    
    suppliers = SupplierLogic.search_suppliers(
        query=search_query, 
        status=status_filter
    )
    
    return render_template('admin/manage_suppliers.html', suppliers=suppliers)

# ==========================================
# 3. محرك تحديث الحالة (Toggle Status)
# ==========================================
@admin_bp.route('/suppliers/toggle/<int:supplier_id>')
@login_required
def toggle_supplier_status(supplier_id):
    # سيتم إضافة منطق تجميد الحساب هنا لاحقاً
    flash("تم تحديث حالة المورد في الترسانة.", "info")
    return redirect(url_for('admin.manage_suppliers'))
