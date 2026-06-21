# coding: utf-8
# 📂 apps/vendor_dashboard/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from apps.models.supplier_profile_db import SupplierProfile

# تعريف الـ Blueprint
dashboard_bp = Blueprint('vendor_dashboard', __name__, template_folder='templates')

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    """
    لوحة تحكم المورد السيادية (محدثة لتتوافق مع الموديلات المشفرة)
    """
    
    # 0. حماية سيادية: التأكد من أن المستخدم الحالي هو مورد
    if not hasattr(current_user, 'supplier_profile'):
        flash("هذا القسم مخصص للموردين فقط.", "error")
        return redirect(url_for('auth_portal.login'))

    # 1. تحقق سيادي: هل يملك المورد بروفايل في قاعدة البيانات؟
    # العلاقة supplier_profile تم تعريفها في الموديل بـ lazy='joined'
    profile = current_user.supplier_profile 
    
    # إذا لم يوجد بروفايل، يجب إكمال الإعداد أولاً
    if not profile:
        return redirect(url_for('vendors.setup_profile'))

    try:
        # جلب البيانات من الموديلات المشفرة بأمان
        # نستغل خصائص الـ @property التي عرفناها في الموديلات لفك التشفير تلقائياً
        recent_orders = [] 
        
        # إحصائيات المورد (يمكن ربطها لاحقاً بقاعدة البيانات)
        supplier_stats = {
            'total_sales': "0.00", 
            'pending_orders': 0
        }
        
    except Exception as e:
        print(f"DEBUG: Dashboard Data Error: {e}")
        recent_orders = []
        supplier_stats = {'total_sales': "0.00", 'pending_orders': 0}

    return render_template(
        'vendor/dashboard.html', 
        profile=profile,
        recent_orders=recent_orders, 
        supplier_stats=supplier_stats
    )

@dashboard_bp.route('/settings')
@login_required
def settings():
    # التحقق من صلاحية الوصول لصفحة الإعدادات
    if not hasattr(current_user, 'supplier_profile'):
        return redirect(url_for('auth_portal.login'))
        
    return "صفحة إعدادات المورد قيد التطوير"
