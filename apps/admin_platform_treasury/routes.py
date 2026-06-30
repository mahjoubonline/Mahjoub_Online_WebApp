# coding: utf-8
# 📂 apps/admin_platform_treasury/routes.py

from flask import Blueprint, render_template, request
from flask_login import login_required
from apps.extensions import db
from .utils import get_treasury_stats, get_filtered_transactions

# تعريف الـ Blueprint مع تحديد المسار الأساسي
treasury_bp = Blueprint('treasury', __name__, template_folder='templates', url_prefix='/admin/treasury')

@treasury_bp.route('/dashboard', methods=['GET'])
@login_required
def treasury_dashboard():
    """
    لوحة تحكم الخزينة: عرض الأرصدة العامة وسجل الحركات المالية الموحد.
    تعتمد على الفلاتر الديناميكية لضمان سرعة الاستعلام.
    """
    # 1. التقاط المدخلات من الفلاتر (UI Filtering)
    currency = request.args.get('currency', 'all')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    page = request.args.get('page', 1, type=int)
    
    # 2. استدعاء الإحصائيات (تعتمد على كود الـ Utils)
    stats = get_treasury_stats(db)
    
    # 3. استدعاء الحركات المفلترة (تستخدم الفهارس (Indexes) التي وضعناها في wallet_db.py)
    query = get_filtered_transactions(
        currency=currency, 
        start_date=start_date, 
        end_date=end_date
    )
    
    # 4. تقسيم الصفحات (Pagination) لضمان عدم ثقل التحميل
    pagination = query.paginate(page=page, per_page=15, error_out=False)
    
    return render_template(
        'admin_platform_treasury.html', 
        stats=stats, 
        transactions=pagination.items, 
        pagination=pagination,
        current_currency=currency,
        start_date=start_date,
        end_date=end_date
    )
