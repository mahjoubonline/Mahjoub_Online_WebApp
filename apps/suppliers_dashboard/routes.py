# coding: utf-8
# 📂 apps/suppliers_dashboard/routes.py

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

# التصحيح هنا: نحدد المجلد الجذر للقوالب ليتمكن من الوصول للمجلد الفرعي 'suppliers'
dashboard_bp = Blueprint(
    'suppliers_dashboard', 
    __name__, 
    template_folder='templates' 
)

@dashboard_bp.route('/')
@login_required
def index():
    """نقطة الدخول للمسار الجذري للمورد (/suppliers/)."""
    if hasattr(current_user, 'wallet') and current_user.wallet is not None:
        return redirect(url_for('suppliers_dashboard.dashboard'))
    return "عذراً، هذا القسم مخصص للموردين فقط."

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    """لوحة تحكم المورد."""
    # التحقق من وجود المحفظة
    if not hasattr(current_user, 'wallet') or current_user.wallet is None:
        return redirect(url_for('suppliers_dashboard.index'))

    # تجهيز البيانات
    pending_orders_count = 0
    if hasattr(current_user, 'orders'):
        pending_orders_count = len([o for o in current_user.orders if o.status == 'pending'])

    # تمرير البيانات للقالب (التأكد من المسار: templates/suppliers/dashboard.html)
    return render_template(
        'suppliers/dashboard.html', 
        pending_orders_count=pending_orders_count
    )

@dashboard_bp.route('/settings')
@login_required
def settings():
    """صفحة إعدادات المتجر للمورد."""
    return render_template('suppliers/settings.html')
