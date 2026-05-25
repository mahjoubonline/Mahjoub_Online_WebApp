# coding: utf-8
from flask import Blueprint, render_template
from flask_login import login_required
from apps.models.supplier_db import Supplier

# تعريف الـ Blueprint الخاص بلوحة التحكم
admin_dashboard = Blueprint('admin_dashboard', __name__, template_folder='templates')

@admin_dashboard.route('/admin/dashboard')
@login_required
def dashboard():
    # جلب إحصائيات النظام
    total_suppliers = Supplier.query.count()
    
    # حساب إجمالي الأرصدة التراكمية لكل الموردين
    all_suppliers = Supplier.query.all()
    total_balance = sum([s.balance for s in all_suppliers])
    
    # إعداد البيانات للعرض
    recent_activities = [] # يمكنك إضافة استعلام لجلب آخر العمليات هنا
    pending_settlements = 0 

    return render_template(
        'admin/dashboard.html',
        total_suppliers=total_suppliers,
        total_balance=total_balance,
        pending_settlements=pending_settlements,
        recent_activities=recent_activities
    )
