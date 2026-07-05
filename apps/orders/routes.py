# coding: utf-8
# 📂 apps/orders/routes.py

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from apps.extensions import db
from apps.models.orders_db import Order
from apps.models.financials_db import OrderFinancial
from apps.orders.services import OrderService  # الخدمة التي تحتوي منطق التسوية
from apps.api.sync_engine import SyncEngine
from sqlalchemy import func

orders_bp = Blueprint('orders', __name__, template_folder='templates')

@orders_bp.route('/dashboard')
@login_required
def dashboard():
    """لوحة تحكم الطلبات - محسنة للأداء العالي."""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # استخدام استعلام واحد لجلب الطلبات مع بياناتها المالية
    query = db.session.query(Order, OrderFinancial).outerjoin(OrderFinancial, Order.id == OrderFinancial.order_id)
    
    # تطبيق الفلاتر
    q = request.args.get('q', '').strip()
    if q:
        query = query.filter(Order.order_id_display.ilike(f'%{q}%') | Order.customer_name.ilike(f'%{q}%'))
    
    status = request.args.get('status', '').strip()
    if status:
        query = query.filter(Order.status == status)
        
    pagination = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # إحصائيات سريعة
    try:
        total_sales = db.session.query(func.sum(OrderFinancial.total_paid_raw)).scalar() or 0
    except Exception as e:
        print(f"⚠️ Error calculating stats: {e}")
        total_sales = 0 
        
    stats = {
        'cancelled': Order.query.filter_by(status='cancelled').count(),
        'completed': Order.query.filter_by(status='completed').count(),
        'total_sales': float(total_sales) 
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('admin/partials/_table.html', pagination=pagination)
    
    return render_template('admin/orders_dashboard.html', pagination=pagination, stats=stats)

@orders_bp.route('/complete-order/<int:order_id>', methods=['POST'])
@login_required
def complete_order(order_id):
    """تسوية الطلب مالياً وتحديث المحفظة تلقائياً."""
    if OrderService.complete_order_and_settle(order_id):
        flash("تمت تسوية الطلب بنجاح وإضافة الرصيد للمحفظة.", "success")
    else:
        flash("فشل في تسوية الطلب أو أن الطلب مسوى مسبقاً.", "danger")
    return redirect(url_for('orders.view_order', order_id=order_id))

@orders_bp.route('/sync-all', methods=['POST'])
@login_required
def sync_all():
    try:
        if SyncEngine.fetch_and_sync_order():
            flash("تم تحديث الطلبات بنجاح.", "success")
        else:
            flash("حدث خطأ أثناء المزامنة.", "danger")
    except Exception as e:
        flash(f"خطأ تقني: {str(e)}", "danger")
    return redirect(url_for('orders.dashboard'))

@orders_bp.route('/view-order/<int:order_id>') 
@login_required
def view_order(order_id):
    order, financial = OrderService.get_order_details(order_id)
    if not order:
        return "الطلب غير موجود", 404
        
    return render_template('admin/order_details.html', order=order, financial=financial)
