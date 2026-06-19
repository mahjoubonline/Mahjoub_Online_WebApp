# coding: utf-8
# 📂 apps/orders/routes.py - النسخة السيادية النهائية (مصححة بالكامل)

from flask import Blueprint, render_template, request, flash, redirect, url_for
from apps.extensions import db
from apps.models.orders_db import ProcessedOrder
from apps.api.sync_engine import SyncEngine
import logging

orders_bp = Blueprint('orders', __name__, url_prefix='/orders', template_folder='templates')
logger = logging.getLogger(__name__)

# 1. لوحة تحكم الطلبات
@orders_bp.route('/dashboard')
def orders_dashboard():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    payment_status = request.args.get('payment_status', '')
    fulfillment_status = request.args.get('fulfillment_status', '')
    
    query = ProcessedOrder.query
    
    # حساب الإجمالي برمجياً لتجنب خطأ قاعدة البيانات مع القيم المشفرة
    all_orders = ProcessedOrder.query.all()
    total_sales = sum(order.total_price for order in all_orders)
    
    completed_count = ProcessedOrder.query.filter_by(fulfillment_status='fulfilled').count()
    cancelled_count = 0 
    
    # تطبيق البحث
    if search:
        query = query.filter(
            (ProcessedOrder.order_id.contains(search)) | 
            (ProcessedOrder.customer_name.contains(search))
        )
    
    # تطبيق الفلاتر
    if payment_status and payment_status != 'all':
        query = query.filter_by(financial_status=payment_status)
    if fulfillment_status and fulfillment_status != 'all':
        query = query.filter_by(fulfillment_status=fulfillment_status)
        
    pagination = query.order_by(ProcessedOrder.created_at_local.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('admin/orders_dashboard.html', 
                           pagination=pagination, 
                           search=search, 
                           payment_status=payment_status,
                           fulfillment_status=fulfillment_status,
                           stats={
                               'total_sales': total_sales,
                               'completed': completed_count,
                               'cancelled': cancelled_count
                           })

# 2. المزامنة الشاملة (المسار المصحح)
@orders_bp.route('/sync-all', methods=['POST'])
def sync_all():
    """دالة المزامنة التي تستدعي الميثود الصحيح من SyncEngine"""
    try:
        # استدعاء الميثود الصحيح بناءً على ما هو موجود في SyncEngine
        SyncEngine.fetch_and_sync_order()
        flash("✅ تمت مزامنة الطلبات بنجاح من قمرة!", "success")
    except Exception as e:
        logger.error(f"❌ خطأ في المزامنة: {e}")
        flash(f"⚠️ حدث خطأ أثناء المزامنة: {e}", "danger")
    
    return redirect(url_for('orders.orders_dashboard'))

# يمكنك إضافة بقية المسارات هنا لاحقاً
