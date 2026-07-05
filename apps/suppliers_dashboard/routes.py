# coding: utf-8
# 📂 apps/suppliers_dashboard/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, session, abort, request
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload
from apps import db 
from apps.models.orders_db import Order 
from apps.models.supplier_db import Supplier

dashboard_bp = Blueprint('suppliers_dashboard', __name__, template_folder='templates')

def full_access_required():
    """
    دالة تحقق مطورة: تسمح للمورد الرئيسي والمالك (Owner) فقط بالوصول الكامل.
    """
    # 1. المورد الرئيسي دائماً لديه وصول كامل
    if session.get('user_type') == 'supplier':
        return
    
    # 2. الموظف: يجب التحقق من دوره (Owner)
    # ملاحظة: تأكد أن نموذج الموظف يحتوي على حقل role
    if session.get('user_type') == 'staff' and getattr(current_user, 'role', None) == 'owner':
        return
        
    abort(403) # منع أي موظف غير المالك

@dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    # جلب المعرف الصحيح
    s_id = current_user.id if session.get('user_type') == 'supplier' else current_user.supplier_id
    
    pending_orders_count = Order.query.filter_by(
        supplier_id=s_id, 
        status='pending'
    ).count()

    return render_template('suppliers/dashboard.html', pending_orders_count=pending_orders_count)

@dashboard_bp.route('/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw():
    full_access_required() 
    flash("سيتم تفعيل خدمة السحب قريباً، يرجى التواصل مع الإدارة.", "info")
    return redirect(url_for('suppliers_dashboard.dashboard'))

@dashboard_bp.route('/settings', methods=['GET'])
@login_required
def settings():
    full_access_required() 
    
    s_id = current_user.id if session.get('user_type') == 'supplier' else current_user.supplier_id
    
    supplier_data = Supplier.query.options(
        joinedload(Supplier.supplier_profile),
        joinedload(Supplier.wallet)
    ).get(s_id)
    
    if not supplier_data:
        abort(404)
        
    return render_template('suppliers/settings.html', current_user=supplier_data)

@dashboard_bp.route('/settings/update', methods=['POST'])
@login_required
def update_settings():
    full_access_required()
    
    # تحديد المورد المستهدف للتحديث
    target = current_user if session.get('user_type') == 'supplier' else current_user.supplier
    profile = target.supplier_profile
    
    if profile:
        profile.owner_name = request.form.get('owner_name')
        profile.email = request.form.get('email')
        profile.phone_secondary = request.form.get('secondary_phone')
        profile.governorate = request.form.get('governorate')
        profile.city = request.form.get('city')
        profile.address = request.form.get('address')
        db.session.commit()
        flash("تم تحديث البيانات بنجاح!", "success")
    return redirect(url_for('suppliers_dashboard.settings'))

@dashboard_bp.route('/settings/update-password', methods=['POST'])
@login_required
def update_password():
    full_access_required()
    
    # التأكد من استخدام المودل الصحيح لتغيير كلمة المرور
    # (إذا كان الموظف يغير كلمة مروره الخاصة، نستخدم current_user مباشرة)
    if current_user.check_password(request.form.get('old_password')):
        current_user.set_password(request.form.get('new_password'))
        db.session.commit()
        flash("تم تغيير كلمة المرور بنجاح!", "success")
    else:
        flash("كلمة المرور الحالية غير صحيحة.", "danger")
    return redirect(url_for('suppliers_dashboard.settings'))
