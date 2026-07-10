# coding: utf-8
# 📂 apps/suppliers_dashboard/routes.py

from flask import Blueprint, render_template, abort, session, request, flash, redirect, url_for
from flask_login import login_required, current_user

# استيراد الموديلات من المركز مباشرة
from apps.models import db, Supplier, Order, SupplierWallet

# تعريف الـ Blueprint
suppliers_dashboard_bp = Blueprint('suppliers_dashboard', __name__, template_folder='templates')

def check_supplier_access():
    """حماية مركزية تمنع الأدمن أو أي مستخدم غريب من ضرب الموديول"""
    user_type = session.get('user_type')
    # إذا كان المستخدم أدمن أو نوعه غير مصرح له هنا
    if hasattr(current_user, 'username') and not hasattr(current_user, 'supplier_id') and user_type != 'supplier':
        return False
    if user_type not in ['supplier', 'staff']:
        return False
    return True

@suppliers_dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """
    لوحة تحكم المورد والموظف بآمان كامل ضد تداخل جلسات الأدمن.
    """
    if not check_supplier_access():
        flash("عذراً، هذا الحساب غير مصرح له بدخول بوابة الموردين.", "danger")
        return redirect(url_for('auth_portal.logout')) # أو تحويله للوحة الأدمن
        
    user_type = session.get('user_type')
    supplier_id = current_user.supplier_id if user_type == 'staff' else current_user.id
    
    supplier = db.session.get(Supplier, supplier_id)
    if not supplier:
        abort(404)
        
    wallet = db.session.execute(
        db.select(SupplierWallet).filter_by(supplier_id=supplier.id)
    ).scalar_one_or_none()
    
    supplier.wallet = wallet
    
    pending_orders_count = Order.query.filter_by(
        supplier_id=supplier.id, 
        status='pending'
    ).count()
    
    return render_template('suppliers/dashboard.html', 
                           supplier=supplier, 
                           pending_orders_count=pending_orders_count)

@suppliers_dashboard_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if not check_supplier_access():
        abort(403)
        
    user_type = session.get('user_type')
    supplier_id = current_user.supplier_id if user_type == 'staff' else current_user.id
    supplier = db.session.get(Supplier, supplier_id)
    
    if not supplier:
        abort(404)
    
    if request.method == 'POST':
        profile = supplier.supplier_profile
        if profile:
            profile.owner_name = request.form.get('owner_name')
            profile.email = request.form.get('email')
            profile.address = request.form.get('address')
        
        try:
            db.session.commit()
            flash('تم تحديث البيانات بنجاح', 'success')
        except Exception:
            db.session.rollback()
            flash('حدث خطأ أثناء حفظ البيانات، حاول مجدداً', 'danger')
            
        return redirect(url_for('suppliers_dashboard.settings'))
        
    return render_template('suppliers/settings.html', supplier=supplier)

@suppliers_dashboard_bp.route('/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw():
    if not check_supplier_access():
        abort(403)
        
    user_type = session.get('user_type')
    supplier_id = current_user.supplier_id if user_type == 'staff' else current_user.id
    supplier = db.session.get(Supplier, supplier_id)
    
    if not supplier:
        abort(404)
        
    wallet = db.session.execute(
        db.select(SupplierWallet).filter_by(supplier_id=supplier.id)
    ).scalar_one_or_none()
    
    supplier.wallet = wallet
    
    return render_template('suppliers/withdraw.html', supplier=supplier)
