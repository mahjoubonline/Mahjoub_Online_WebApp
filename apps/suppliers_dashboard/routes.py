# coding: utf-8
from flask import Blueprint, render_template, abort, session, request, flash, redirect, url_for
from flask_login import login_required, current_user
from apps.models.supplier_db import Supplier, db # افترضنا وجود db هنا

# تعريف الـ Blueprint
suppliers_dashboard_bp = Blueprint('suppliers_dashboard', __name__, template_folder='templates')

# إضافة القائمة الجانبية ديناميكياً لجميع صفحات الداشبورد
@suppliers_dashboard_bp.context_processor
def inject_sidebar_modules():
    modules = {
        'dashboard': {
            'display_name': 'لوحة التحكم', 
            'icon': 'fas fa-tachometer-alt', 
            'links': {'main': 'suppliers_dashboard.dashboard'}
        },
        'settings': {
            'display_name': 'إعدادات المتجر', 
            'icon': 'fas fa-cog', 
            'links': {'main': 'suppliers_dashboard.settings'}
        }
    }
    return dict(supplier_modules=modules)

@suppliers_dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    if session.get('user_type') != 'supplier':
        abort(403)
        
    supplier = Supplier.query.get(current_user.id)
    
    # حساب الطلبات المعلقة (مثال بناءً على علاقة الـ orders)
    pending_orders_count = 0
    if hasattr(supplier, 'orders'):
        pending_orders_count = supplier.orders.filter_by(status='pending').count()
    
    return render_template('suppliers/dashboard.html', 
                           supplier=supplier, 
                           pending_orders_count=pending_orders_count)

@suppliers_dashboard_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if session.get('user_type') != 'supplier':
        abort(403)
        
    supplier = Supplier.query.get(current_user.id)
    
    # معالجة تحديث البيانات
    if request.method == 'POST':
        # هنا يتم تحديث بيانات الملف الشخصي
        profile = supplier.supplier_profile
        profile.owner_name = request.form.get('owner_name')
        profile.email = request.form.get('email')
        profile.address = request.form.get('address')
        db.session.commit()
        flash('تم تحديث البيانات بنجاح', 'success')
        return redirect(url_for('suppliers_dashboard.settings'))
        
    return render_template('suppliers/settings.html', supplier=supplier)

# ملاحظة: تأكد من إضافة دالة withdraw لاحقاً عند البدء في برمجة نظام السحب
