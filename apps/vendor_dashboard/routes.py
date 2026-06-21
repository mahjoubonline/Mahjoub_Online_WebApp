# coding: utf-8
# 📂 apps/vendor_dashboard/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from apps import db
# سنفترض وجود موديلات الطلبات، يمكنك استبدالها بما لديك
# من apps.models.order_db import Order 

dashboard_bp = Blueprint('vendor_dashboard', __name__, template_folder='templates')

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    """
    لوحة تحكم المورد السيادية:
    1. تتحقق من اكتمال البيانات (is_setup_complete).
    2. تمرر البيانات للمورد بأمان.
    """
    
    # التحقق من حالة المورد (هل أكمل ملفه الشخصي؟)
    # إذا لم تكن الخاصية موجودة في الموديل، نعتبره غير مكتمل
    is_ready = getattr(current_user, 'is_setup_complete', False)
    
    if not is_ready:
        # توجيه المورد لصفحة الإعداد إذا لم يكمل بياناته
        return redirect(url_for('vendors.setup_profile'))

    # جلب البيانات المطلوبة للوحة التحكم
    try:
        # ملاحظة: قم بتعديل هذا الجزء ليتناسب مع أسماء الموديلات لديك
        # recent_orders = Order.query.filter_by(supplier_id=current_user.id).order_by(Order.created_at.desc()).limit(5).all()
        recent_orders = [] # افتراضي فارغ لتجنب الخطأ
        
        # إحصائيات المورد
        supplier_stats = {
            'total_sales': "0.00",
            'pending_orders': 0
        }
    except Exception as e:
        # في حال حدوث أي خطأ في قاعدة البيانات، نعرض اللوحة بدون بيانات بدلاً من انهيار النظام
        print(f"DEBUG: Dashboard Data Error: {e}")
        recent_orders = []
        supplier_stats = {'total_sales': "0.00", 'pending_orders': 0}

    return render_template(
        'vendor/dashboard.html', 
        recent_orders=recent_orders, 
        supplier_stats=supplier_stats
    )

@dashboard_bp.route('/settings')
@login_required
def settings():
    return "صفحة إعدادات المورد قيد التطوير"
