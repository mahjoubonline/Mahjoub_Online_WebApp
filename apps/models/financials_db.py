# coding: utf-8
# 📂 apps/orders/routes.py - النسخة النهائية المحدثة

from flask import Blueprint, render_template, request, flash, redirect, url_for, session, abort, current_app
from flask_login import login_required
from datetime import datetime
from sqlalchemy import func
from apps.extensions import db
from apps.models.orders_db import Order
from apps.models.financials_db import OrderFinancial
from apps.models.supplier_db import Supplier
from apps.orders.services import OrderService
from apps.api.sync_engine import SyncEngine 
import logging

logger = logging.getLogger(__name__)

orders_bp = Blueprint('orders', __name__, template_folder='templates')

def admin_required():
    """التحقق من صلاحية المسؤول"""
    if session.get('user_type') != 'admin':
        abort(403)

@orders_bp.route('/dashboard')
@login_required
def dashboard():
    admin_required()
    
    # التحقق من توفر المسارات
    can_add_order = 'orders.add_new_order' in current_app.view_functions
    can_sync = 'orders.sync_all' in current_app.view_functions
    
    # إحصائيات اللوحة - استخدام total_paid_raw للعمليات الحسابية الآمنة والسريعة
    total_sales = db.session.query(func.sum(OrderFinancial.total_paid_raw)).scalar() or 0
    completed_count = Order.query.filter_by(status='completed').count()
    cancelled_count = Order.query.filter_by(status='cancelled').count()
    
    stats = {
        'total_sales': float(total_sales),
        'completed': completed_count,
        'cancelled': cancelled_count
    }
    
    # الترقيم (Pagination)
    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Order, OrderFinancial)\
        .outerjoin(OrderFinancial, Order.id == OrderFinancial.order_id)\
        .order_by(Order.id.desc())\
        .paginate(page=page, per_page=20)
    
    return render_template('admin/orders_dashboard.html', 
                           pagination=pagination, 
                           stats=stats,
                           can_add_order=can_add_order,
                           can_sync=can_sync)

@orders_bp.route('/sync-all', methods=['POST'])
@login_required
def sync_all():
    """تشغيل المزامنة اليدوية مع منصة قمرة"""
    admin_required()
    try:
        if SyncEngine.run_manual_sync():
            flash("تمت عملية المزامنة بنجاح وجلب الطلبات الجديدة.", "success")
        else:
            flash("لم يتم جلب بيانات جديدة أو حدث خطأ أثناء المزامنة.", "warning")
