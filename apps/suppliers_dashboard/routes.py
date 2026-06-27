# coding: utf-8
# 📂 apps/suppliers_dashboard/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
# استيراد النماذج (تأكد من تعديل المسارات حسب هيكل مجلداتك)
from apps.models import Order 

# تعريف البلوبرينت
dashboard_bp = Blueprint(
    'suppliers_dashboard', 
    __name__, 
    template_folder='templates'
)

@dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """
    لوحة التحكم الرئيسية للمورد.
    يتم جلب عدد الطلبات المعلقة فعلياً من قاعدة البيانات.
    """
    # جلب عدد الطلبات التي حالتها 'pending' والتابعة لهذا المورد
    pending_orders_count = Order.query.filter_by(
        supplier_id=current_user.id, 
        status='pending'
    ).count()

    context = {
        'pending_orders_count': pending_orders_count,
        # current_user متاح تلقائياً في القوالب
    }
    
    return render_template('suppliers/dashboard.html', **context)

@dashboard_bp.route('/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw():
    """
    مسار طلب سحب الرصيد.
    """
    # حالياً نقوم بإعادة التوجيه، لاحقاً سنضيف منطق إنشاء طلب السحب (WithdrawalRequest)
    flash("سيتم تفعيل خدمة السحب قريباً، يرجى التواصل مع الإدارة.", "info")
    return redirect(url_for('suppliers_dashboard.dashboard'))

@dashboard_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """
    صفحة إعدادات المتجر الخاصة بالمورد.
    """
    return render_template('suppliers/settings.html')
