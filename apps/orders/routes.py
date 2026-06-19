# coding: utf-8
# 📂 apps/orders/routes.py - النسخة السيادية النهائية المحدثة

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from apps.extensions import db
from apps.models.orders_db import ProcessedOrder
from apps.api.sync_engine import SyncEngine
import logging

orders_bp = Blueprint('orders', __name__, url_prefix='/orders', template_folder='templates')
logger = logging.getLogger(__name__)

# 1. لوحة تحكم الطلبات (مع دعم البحث والفلاتر والترقيم والإحصائيات)
@orders_bp.route('/dashboard')
def orders_dashboard():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    payment_status = request.args.get('payment_status', '')
    fulfillment_status = request.args.get('fulfillment_status', '')
    
    query = ProcessedOrder.query
    
    # --- التعديل الأساسي لحل خطأ "can't adapt type property" ---
    # جلب جميع الطلبات لحساب الإجمالي برمجياً لأن قاعدة البيانات لا تستطيع التعامل مع البيانات المشفرة
    all_orders = ProcessedOrder.query.all()
    total_sales = sum(order.total_price for order in all_orders)
    
    # إحصائيات الحالة
    completed_count = ProcessedOrder.query.filter_by(fulfillment_status='fulfilled').count()
    cancelled_count = 0 
    # -----------------------------------------------------------
    
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

# (بقية المسارات: sync_all, update_order_field, delete_order, process_order, download_invoice)
# تبقى كما هي في كودك فهي ممتازة ولا تحتاج تعديل.
