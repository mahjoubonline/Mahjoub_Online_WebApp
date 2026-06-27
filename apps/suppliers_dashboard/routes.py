# coding: utf-8
# 📂 apps/suppliers_dashboard/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, session, abort, request
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload

# استيراد قاعدة البيانات والنماذج
from apps import db 
from apps.models.orders_db import Order 
from apps.models.supplier_db import Supplier

# تعريف البلوبرينت
dashboard_bp = Blueprint(
    'suppliers_dashboard', 
    __name__, 
    template_folder='templates'
)

def supplier_required():
    """
    دالة تحقق أمني: تضمن أن المستخدم الحالي مورد.
    """
    if session.get('user_type') != 'supplier':
        abort(403)

@dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """
    لوحة التحكم الرئيسية للمورد.
    """
    supplier_required() 
    
    # جلب عدد الطلبات المعلقة فعلياً
    pending_orders_count = Order.query.filter_by(
        supplier_id=current_user.id, 
        status='pending'
    ).count()

    return render_template('suppliers/dashboard.html', pending_orders_count=pending_orders_count)

@dashboard_bp.route('/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw():
    supplier_required() 
    flash("سيتم تفعيل خدمة السحب قريباً، يرجى التواصل مع الإدارة.", "info")
    return redirect(url_for('suppliers_dashboard.dashboard'))

@dashboard_bp.route('/settings', methods=['GET'])
@login_required
def settings():
    """
    صفحة إعدادات المتجر مع جلب بيانات الملف الشخصي والمحفظة.
    """
    supplier_required() 
    
    # جلب المورد مع بيانات الملف الشخصي والمحفظة المرتبطة به
    supplier_data = Supplier.query.options(
        joinedload(Supplier.supplier_profile),
        joinedload(Supplier.wallet)
    ).get(current_user.id)
    
    if not supplier_data:
        abort(404)
        
    return render_template('suppliers/settings.html', current_user=supplier_data)

@dashboard_bp.route('/settings/update', methods=['POST'])
@login_required
def update_settings():
    """
    تحديث بيانات الملف الشخصي للمورد.
    """
    supplier_required()
    
    profile = current_user.supplier_profile
    
    if profile:
        profile.owner_name = request.form.get('owner_name')
        profile.email = request.form.get('email')
        profile.phone_secondary = request.form.get('secondary_phone')
        profile.governorate = request.form.get('governorate')
        profile.city = request.form.get('city')
        profile.address = request.form.get('address')
        
        db.session.commit()
        flash("تم تحديث بيانات ملفك الشخصي بنجاح!", "success")
    else:
        flash("خطأ: تعذر الوصول إلى بيانات الملف الشخصي.", "danger")
    
    return redirect(url_for('suppliers_dashboard.settings'))

@dashboard_bp.route('/settings/update-password', methods=['POST'])
@login_required
def update_password():
    """
    تغيير كلمة المرور الخاصة بالمورد.
    """
    supplier_required()
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    
    # التحقق من كلمة المرور القديمة باستخدام دالة النموذج
    if current_user.check_password(old_password):
        current_user.set_password(new_password)
        db.session.commit()
        flash("تم تغيير كلمة المرور بنجاح!", "success")
    else:
        flash("كلمة المرور الحالية غير صحيحة، يرجى المحاولة مرة أخرى.", "danger")
        
    return redirect(url_for('suppliers_dashboard.settings'))
