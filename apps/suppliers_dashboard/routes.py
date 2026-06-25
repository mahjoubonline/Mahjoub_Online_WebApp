# coding: utf-8
# 📂 apps/suppliers_dashboard/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

dashboard_bp = Blueprint(
    'suppliers_dashboard', 
    __name__, 
    template_folder='templates'
)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    """
    لوحة تحكم المورد مع حماية ضد الخطأ في حال لم يكن المستخدم مورداً.
    """
    
    # حماية: التحقق من أن المستخدم لديه علاقة محفظة (يعني أنه مورد)
    if not hasattr(current_user, 'wallet') or current_user.wallet is None:
        # إذا كان مديراً أو مستخدماً ليس له محفظة، نمنعه أو نوجهه
        flash("هذه الصفحة مخصصة للموردين فقط.", "danger")
        return redirect(url_for('main.index')) # أو أي صفحة مناسبة

    # جلب البيانات بأمان
    wallet = current_user.wallet 
    
    # حساب الطلبات (مع التأكد من وجود البيانات)
    pending_orders_count = 0
    if hasattr(current_user, 'orders') and current_user.orders:
        pending_orders_count = len([o for o in current_user.orders if o.status == 'pending'])
    
    # حساب إجمالي المبيعات
    total_sales = 0.00
    if hasattr(current_user, 'financials') and current_user.financials:
        total_sales = sum(float(f.amount) for f in current_user.financials if f.status == 'completed')

    return render_template(
        'suppliers/dashboard.html', 
        wallet=wallet,
        pending_orders_count=pending_orders_count,
        total_sales=total_sales
    )

@dashboard_bp.route('/settings')
@login_required
def settings():
    return render_template('suppliers/settings.html')

@dashboard_bp.route('/')
@login_required
def index():
    return redirect(url_for('suppliers_dashboard.dashboard'))
